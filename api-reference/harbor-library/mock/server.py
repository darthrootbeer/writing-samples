#!/usr/bin/env python3
"""Sandbox for the Harbor Library Lending API.

Standard library only. Run it:   python3 mock/server.py [port]
It listens on http://127.0.0.1:8080 by default and answers the same requests the
documentation shows, with the same data. The clock is fixed at 2026-10-26 so the
examples give the same answer every time.

Sandbox rules (also in docs/authentication.md and docs/rate-limits.md):
  - The only accepted API key is  hl_test_sandbox
  - Send  X-Sandbox-Force: rate_limited  to get the 429 response on demand.
  - State lives in memory. Restart the server to reset it.
"""
import copy
import json
import sys
from datetime import date, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TODAY = date(2026, 10, 26)
API_KEY = "hl_test_sandbox"
LOAN_DAYS = 21
RENEW_DAYS = 14
MAX_RENEWALS = 2
FINE_LIMIT_CENTS = 1000
DOCS = "https://docs.harborlibrary.example/errors#"


def fresh_state():
    return {
        "members": {
            "mem_ada": {"id": "mem_ada", "name": "Ada Lovelace", "card_status": "active", "fines_cents": 0},
            "mem_grace": {"id": "mem_grace", "name": "Grace Hopper", "card_status": "active", "fines_cents": 0},
            "mem_rip": {"id": "mem_rip", "name": "Rip Van Winkle", "card_status": "blocked", "fines_cents": 124000},
        },
        "books": {
            "bk_001": {"id": "bk_001", "title": "Frankenstein", "author": "Mary Shelley", "copies_total": 2, "copies_available": 1},
            "bk_002": {"id": "bk_002", "title": "A Wizard of Earthsea", "author": "Ursula K. Le Guin", "copies_total": 1, "copies_available": 0},
            "bk_003": {"id": "bk_003", "title": "The Left Hand of Darkness", "author": "Ursula K. Le Guin", "copies_total": 3, "copies_available": 3},
            "bk_004": {"id": "bk_004", "title": "Kindred", "author": "Octavia E. Butler", "copies_total": 1, "copies_available": 1},
            "bk_042": {"id": "bk_042", "title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "copies_total": 42, "copies_available": 42},
        },
        "loans": {
            "loan_0001": {"id": "loan_0001", "member_id": "mem_rip", "book_id": "bk_001", "status": "overdue",
                          "borrowed_on": "2006-03-14", "due_on": "2006-04-04", "returned_on": None, "renewals": 0},
            "loan_0002": {"id": "loan_0002", "member_id": "mem_ada", "book_id": "bk_002", "status": "active",
                          "borrowed_on": "2026-10-12", "due_on": "2026-11-02", "returned_on": None, "renewals": 0},
            "loan_0003": {"id": "loan_0003", "member_id": "mem_ada", "book_id": "bk_003", "status": "returned",
                          "borrowed_on": "2026-08-10", "due_on": "2026-08-31", "returned_on": "2026-08-28", "renewals": 0},
            "loan_0004": {"id": "loan_0004", "member_id": "mem_grace", "book_id": "bk_004", "status": "active",
                          "borrowed_on": "2026-09-30", "due_on": "2026-10-21", "returned_on": None, "renewals": 2},
        },
        "next_loan": 5,
        "next_request": 1,
        "idempotency": {},
    }


STATE = fresh_state()


class ApiError(Exception):
    def __init__(self, status, code, message, param=None):
        self.status, self.code, self.message, self.param = status, code, message, param


def page(items, query):
    """Cursor pagination. A cursor is opaque to clients; here it encodes an offset."""
    try:
        limit = int(query.get("limit", "20"))
    except ValueError:
        raise ApiError(400, "invalid_request", "limit must be a whole number from 1 to 100.", "limit")
    if not 1 <= limit <= 100:
        raise ApiError(400, "invalid_request", "limit must be a whole number from 1 to 100.", "limit")
    start = 0
    cursor = query.get("cursor")
    if cursor:
        if not cursor.startswith("cur_") or not cursor[4:].isdigit():
            raise ApiError(400, "invalid_cursor", "That cursor is not valid. Use next_cursor exactly as the last response returned it.", "cursor")
        start = int(cursor[4:])
    chunk = items[start:start + limit]
    more = start + limit < len(items)
    return {"data": chunk, "has_more": more, "next_cursor": f"cur_{start + limit}" if more else None}


def refresh_status(loan):
    if loan["status"] == "active" and date.fromisoformat(loan["due_on"]) < TODAY:
        loan["status"] = "overdue"
    return loan


def get_book(book_id):
    book = STATE["books"].get(book_id)
    if not book:
        raise ApiError(404, "book_not_found", f"No book has the id {book_id}.", "book_id")
    return book


def get_member(member_id):
    member = STATE["members"].get(member_id)
    if not member:
        raise ApiError(404, "member_not_found", f"No member has the id {member_id}.", "member_id")
    return dict(member, open_loans=sum(1 for l in STATE["loans"].values()
                                      if l["member_id"] == member_id and l["status"] != "returned"))


def get_loan(loan_id):
    loan = STATE["loans"].get(loan_id)
    if not loan:
        raise ApiError(404, "loan_not_found", f"No loan has the id {loan_id}.", "loan_id")
    return refresh_status(loan)


def check_lend_body(body):
    for field in ("member_id", "book_id"):
        if field not in body or body[field] in (None, ""):
            raise ApiError(400, "invalid_request", f"{field} is required.", field)
        if not isinstance(body[field], str):
            raise ApiError(400, "invalid_request", f"{field} must be a string.", field)


def parse_json_object(raw):
    if not raw:
        return {}
    try:
        body = json.loads(raw)
    except json.JSONDecodeError:
        raise ApiError(400, "invalid_json", "The request body is not valid JSON.")
    if not isinstance(body, dict):
        raise ApiError(400, "invalid_json", "The request body must be a JSON object.")
    return body


def create_loan(body):
    member = get_member(body["member_id"])
    book = get_book(body["book_id"])
    if member["card_status"] == "blocked":
        dollars = member["fines_cents"] / 100
        raise ApiError(403, "member_blocked",
                       f"{member['name']} owes ${dollars:,.2f} in fines. A card with more than $10.00 in fines is blocked.", "member_id")
    if book["copies_available"] < 1:
        raise ApiError(409, "book_unavailable", f"All copies of \"{book['title']}\" are on loan.", "book_id")
    book["copies_available"] -= 1
    loan_id = f"loan_{STATE['next_loan']:04d}"
    STATE["next_loan"] += 1
    loan = {"id": loan_id, "member_id": member["id"], "book_id": book["id"], "status": "active",
            "borrowed_on": TODAY.isoformat(), "due_on": (TODAY + timedelta(days=LOAN_DAYS)).isoformat(),
            "returned_on": None, "renewals": 0}
    STATE["loans"][loan_id] = loan
    return loan


def renew_loan(loan):
    if loan["status"] == "returned":
        raise ApiError(409, "loan_not_active", f"{loan['id']} was already returned on {loan['returned_on']}.", "loan_id")
    if loan["status"] == "overdue":
        raise ApiError(409, "loan_overdue", f"{loan['id']} is overdue. Return the book first. An overdue loan cannot be renewed.", "loan_id")
    if loan["renewals"] >= MAX_RENEWALS:
        raise ApiError(409, "renewal_limit_reached", f"{loan['id']} has used all {MAX_RENEWALS} renewals.", "loan_id")
    loan["renewals"] += 1
    loan["due_on"] = (date.fromisoformat(loan["due_on"]) + timedelta(days=RENEW_DAYS)).isoformat()
    return loan


def return_loan(loan):
    if loan["status"] == "returned":
        raise ApiError(409, "loan_not_active", f"{loan['id']} was already returned on {loan['returned_on']}.", "loan_id")
    loan["status"] = "returned"
    loan["returned_on"] = TODAY.isoformat()
    STATE["books"][loan["book_id"]]["copies_available"] += 1
    return loan


class Handler(BaseHTTPRequestHandler):
    server_version = "HarborSandbox/1.0"

    def log_message(self, *args):
        pass

    def send(self, status, body, extra=None):
        payload = json.dumps(body, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("X-Request-Id", self.request_id)
        self.send_header("X-Librarian", "Marian")
        extra = dict(extra or {})
        self.send_header("X-RateLimit-Limit", "60")
        self.send_header("X-RateLimit-Remaining", extra.pop("X-RateLimit-Remaining", "59"))
        for k, v in extra.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(payload)

    def fail(self, e, extra=None):
        err = {"status": e.status, "code": e.code, "message": e.message}
        if e.param:
            err["param"] = e.param
        err["doc_url"] = DOCS + e.code
        err["request_id"] = self.request_id
        self.send(e.status, {"error": err}, extra)

    def handle_any(self, method):
        self.request_id = f"req_{STATE['next_request']:06d}"
        STATE["next_request"] += 1
        path, _, qs = self.path.partition("?")
        query = dict(p.split("=", 1) if "=" in p else (p, "") for p in qs.split("&") if p)
        try:
            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length else b""

            if path == "/v1/teapot":  # Easter egg: see docs/easter-eggs.md. Needs no key.
                if method != "GET":
                    raise ApiError(405, "method_not_allowed", f"{method} is not allowed at {path}.")
                raise ApiError(418, "teapot", "I'm a teapot, short and stout. The library does not brew coffee.")

            auth = self.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                raise ApiError(401, "unauthorized", "Send your API key as: Authorization: Bearer YOUR_KEY.")
            if auth[7:] != API_KEY:
                raise ApiError(401, "invalid_api_key", "That API key is not recognized.")

            if self.headers.get("X-Sandbox-Force") == "rate_limited":  # Easter egg: the 429 is "shush"
                raise_rate = ApiError(429, "shush", "Shh. This is a library. Wait a moment, then try again.")
                self.fail(raise_rate, {"Retry-After": "3", "X-RateLimit-Remaining": "0"})
                return

            parts = [p for p in path.split("/") if p]
            if len(parts) < 2 or parts[0] != "v1":
                raise ApiError(404, "route_not_found", f"There is no endpoint at {path}.")
            res = parts[1]
            rid = parts[2] if len(parts) > 2 else None
            action = parts[3] if len(parts) > 3 else None

            if res == "books" and method == "GET" and not rid:
                items = list(STATE["books"].values())
                q = query.get("q", "").replace("%20", " ").replace("+", " ").lower()
                if q:
                    items = [b for b in items if q in b["title"].lower() or q in b["author"].lower()]
                if "available" in query and query["available"] not in ("true", "false"):
                    raise ApiError(400, "invalid_request", "available must be true or false.", "available")
                if query.get("available") == "true":
                    items = [b for b in items if b["copies_available"] > 0]
                return self.send(200, page(items, query))
            if res == "books" and method == "GET" and rid and not action:
                return self.send(200, get_book(rid))
            if res == "members" and method == "GET" and rid and not action:
                return self.send(200, get_member(rid))
            if res == "loans" and method == "GET" and not rid:
                items = [refresh_status(l) for l in STATE["loans"].values()]
                if "member_id" in query:
                    items = [l for l in items if l["member_id"] == query["member_id"]]
                if "status" in query:
                    if query["status"] not in ("active", "overdue", "returned"):
                        raise ApiError(400, "invalid_request", "status must be active, overdue, or returned.", "status")
                    items = [l for l in items if l["status"] == query["status"]]
                return self.send(200, page(items, query))
            if res == "loans" and method == "GET" and rid and not action:
                return self.send(200, get_loan(rid))
            if res == "loans" and method == "POST" and not rid:
                body = parse_json_object(raw)
                check_lend_body(body)
                key = self.headers.get("Idempotency-Key")
                if key is not None and not 1 <= len(key) <= 64:
                    raise ApiError(400, "invalid_request", "Idempotency-Key must be 1 to 64 characters.", "Idempotency-Key")
                if key and key in STATE["idempotency"]:
                    first_body, saved = STATE["idempotency"][key]
                    if first_body != body:
                        raise ApiError(409, "idempotency_key_reused",
                                       "That Idempotency-Key was already used with a different request. Use a new key.", "Idempotency-Key")
                    return self.send(201, saved, {"Idempotent-Replay": "true", "Location": f"/v1/loans/{saved['id']}"})
                loan = create_loan(body)
                if key:  # only a successful lend is stored; a failed request can be retried with the same key
                    STATE["idempotency"][key] = (copy.deepcopy(body), copy.deepcopy(loan))
                return self.send(201, loan, {"Location": f"/v1/loans/{loan['id']}"})
            if res == "loans" and method == "POST" and rid and action == "renew":
                return self.send(200, renew_loan(get_loan(rid)))
            if res == "loans" and method == "POST" and rid and action == "return":
                return self.send(200, return_loan(get_loan(rid)))
            if res in ("books", "members", "loans", "teapot"):
                raise ApiError(405, "method_not_allowed", f"{method} is not allowed at {path}.")
            raise ApiError(404, "route_not_found", f"There is no endpoint at {path}.")
        except ApiError as e:
            self.fail(e)

    def do_GET(self):
        self.handle_any("GET")

    def do_POST(self):
        self.handle_any("POST")

    def do_HEAD(self):
        self.handle_any("HEAD")

    def do_OPTIONS(self):
        self.handle_any("OPTIONS")

    def do_PUT(self):
        self.handle_any("PUT")

    def do_PATCH(self):
        self.handle_any("PATCH")

    def do_DELETE(self):
        self.handle_any("DELETE")


def serve(port=8080):
    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print(f"Harbor Library sandbox on http://127.0.0.1:{port}  (API key: {API_KEY})", flush=True)
    serve(port).serve_forever()
