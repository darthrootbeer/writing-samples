#!/usr/bin/env python3
"""Run every curl example in the Harbor Library docs against the sandbox.

    python3 api-reference/harbor-library/tests/run_examples.py            # check
    python3 api-reference/harbor-library/tests/run_examples.py --update   # rewrite the saved responses

A bash block that starts with `curl` and is followed by a json block is one example.
The json block is the response the docs promise. The check runs the request against
the sandbox and fails if the answer differs, or if the status is not one the OpenAPI
file lists for that route. Each page runs against a fresh sandbox, top to bottom, so
a page may rely on what an earlier example on the same page did.

It also checks that every error code in the sandbox has its own heading in docs/errors.md, and that every link to a section of that page lands on a real heading.
"""
import json
import pathlib
import re
import shlex
import subprocess
import sys
import threading

import yaml

HERE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "mock"))
import server  # noqa: E402

BASE = "http://127.0.0.1:8080"
PAGES = ["docs/quickstart.md", "docs/authentication.md", "docs/pagination.md", "docs/idempotency.md",
         "docs/reference/books.md", "docs/reference/members.md", "docs/reference/loans.md",
         "docs/errors.md", "docs/rate-limits.md", "docs/easter-eggs.md"]
FENCE = re.compile(r"^```(\w*)\s*$")


def blocks(lines):
    """Yield (lang, start, end, body) for every fenced block. start/end are line indexes of the fences."""
    i = 0
    while i < len(lines):
        m = FENCE.match(lines[i])
        if m and m.group(1):
            j = i + 1
            while j < len(lines) and not FENCE.match(lines[j]):
                j += 1
            yield m.group(1), i, j, "\n".join(lines[i + 1:j])
            i = j + 1
        else:
            i += 1


def run_curl(cmd, port):
    cmd = cmd.replace("\\\n", " ").replace(BASE, f"http://127.0.0.1:{port}")
    args = shlex.split(cmd)
    out = subprocess.run(args[:1] + ["-s", "-w", "\n%{http_code}"] + args[1:], capture_output=True, text=True, timeout=20)
    body, _, status = out.stdout.rpartition("\n")
    return int(status), json.loads(body)


def mask(obj):
    if isinstance(obj, dict):
        return {k: ("<id>" if k == "request_id" else mask(v)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [mask(v) for v in obj]
    return obj


def route_statuses(spec):
    table = []
    for path, ops in spec["paths"].items():
        rx = re.compile("^" + re.sub(r"\{[^}]+\}", "[^/]+", path) + "$")
        for method, op in ops.items():
            table.append((method.upper(), rx, {int(c) for c in op["responses"]}))
    return table


def main(update=False):
    spec = yaml.safe_load((HERE / "openapi.yaml").read_text())
    routes = route_statuses(spec)
    httpd = server.serve(0)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    problems, count = [], 0

    for page in PAGES:
        path = HERE / page
        lines = path.read_text(encoding="utf-8").split("\n")
        server.STATE = server.fresh_state()
        found = list(blocks(lines))
        edits = []
        for k, (lang, s, e, body) in enumerate(found):
            if lang != "bash" or not body.lstrip().startswith("curl"):
                continue
            if k + 1 >= len(found) or found[k + 1][0] != "json":
                problems.append(f"{page}:{s + 1}: curl example has no json response block after it")
                continue
            count += 1
            status, actual = run_curl(body, port)
            _, js, je, saved = found[k + 1]
            method = "POST" if re.search(r"-X\s+POST|\s-d\s|--data", body) else "GET"
            url_path = re.search(re.escape(BASE) + r"(/[^\s?'\"]*)", body).group(1).replace("/v1", "", 1)
            ok_routes = [r for r in routes if r[0] == method and r[1].match(url_path)]
            if ok_routes and status not in ok_routes[0][2]:
                problems.append(f"{page}:{s + 1}: status {status} is not listed in openapi.yaml for {method} {url_path}")
            if update:
                edits.append((js, je, json.dumps(actual, indent=2)))
            elif mask(json.loads(saved)) != mask(actual):
                problems.append(f"{page}:{s + 1}: the response in the docs does not match the sandbox (status {status})")
        for js, je, text in reversed(edits):
            lines[js + 1:je] = text.split("\n")
        if update:
            path.write_text("\n".join(lines), encoding="utf-8")

    errors_doc = (HERE / "docs/errors.md").read_text(encoding="utf-8")
    src = (HERE / "mock/server.py").read_text(encoding="utf-8")
    codes = set(re.findall(r'ApiError\(\d+,\s*"([a-z_]+)"', src)) | {"shush"}
    for code in sorted(codes):
        if f"`{code}`" not in errors_doc:
            problems.append(f"docs/errors.md: the sandbox can return `{code}` but the page never names it")

    # Every link to a section of the errors page must land on a real heading.
    def slug(h):
        return re.sub(r"[^a-z0-9_ -]", "", h.lower()).strip().replace(" ", "-")
    anchors = {slug(h) for h in re.findall(r"(?m)^#{1,6} (.+)$", errors_doc)}
    for page in PAGES + ["README.md"]:
        for m in re.finditer(r"errors\.md#([A-Za-z0-9_-]+)|\]\(#([A-Za-z0-9_-]+)\)", (HERE / page).read_text(encoding="utf-8")):
            target = m.group(1) or (m.group(2) if page == "docs/errors.md" else None)
            if target and target not in anchors:
                problems.append(f"{page}: links to errors.md#{target}, which is not a heading on that page")
    for code in sorted(codes):
        if code not in anchors:
            problems.append(f"docs/errors.md: no heading for `{code}`, so the doc_url the API sends lands nowhere")

    httpd.shutdown()
    if problems:
        print(f"run_examples: {len(problems)} problem(s)")
        for p in problems:
            print("  " + p)
        return 1
    print(f"run_examples: clean ({count} examples run against the sandbox)")
    return 0


if __name__ == "__main__":
    sys.exit(main("--update" in sys.argv))
