# Harbor Library Lending API: a documentation sample

A complete, small API reference for a library lending service: quickstart, authentication, pagination, reference pages, errors, rate limits, and a changelog. The API is made up. **Every example in these pages runs.**

**Written for** developers who build against an API and want to see how I document one. **To show** the parts of API documentation that decide whether a developer succeeds on the first try: a working first call, an errors page that tells you what to do next, and examples that cannot drift from the truth.

## What to open first

1. [Quickstart](docs/quickstart.md): a first loan in about five minutes.
2. [Errors](docs/errors.md): every error code, its cause, and its fix.
3. [Loans reference](docs/reference/loans.md): the endpoint with the most going on.
4. [OpenAPI file](openapi.yaml): the source of truth the pages follow.

The rest: [Authentication](docs/authentication.md), [Idempotency](docs/idempotency.md), [Pagination](docs/pagination.md), [Books](docs/reference/books.md), [Members](docs/reference/members.md), [Rate limits](docs/rate-limits.md), [Changelog](docs/changelog.md), and [Easter eggs](docs/easter-eggs.md), which are real and listed so nobody mistakes them for bugs.

## Why the examples cannot go stale

`mock/server.py` is a sandbox with no dependencies. `tests/run_examples.py` finds every `curl` example in the pages, runs it against the sandbox, and fails if the answer differs from the response shown. It also fails if a status is not one the OpenAPI file lists for that route, or if an error code the sandbox can return is missing from the errors page. A GitHub Action runs it on every change.

Each page assumes a fresh sandbox, and the check restarts the sandbox for every page. Run it yourself:

```bash
pip install pyyaml
python3 api-reference/harbor-library/tests/run_examples.py
```

## How this was made

I designed the API and directed the work. An AI tool (Claude) drafted the pages and the sandbox. Four AI reader personas then reviewed the pages over several rounds, and I edited and approved the result. The sandbox and the checks are what keep the AI-drafted parts honest.

The library, its members, and its books are invented. Real authors and titles appear only as sample data.
