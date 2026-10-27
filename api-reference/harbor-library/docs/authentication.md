# Authentication

**Written for** a developer who is about to make the first real call, **to** send the API key correctly and understand the two ways it can fail.

Every endpoint except the [teapot](easter-eggs.md) needs an API key. Send it in the `Authorization` header with the word `Bearer` in front. `Bearer` means "whoever carries this key is allowed in."

```bash
curl "http://127.0.0.1:8080/v1/members/mem_ada" \
  -H "Authorization: Bearer hl_test_sandbox"
```

```json
{
  "id": "mem_ada",
  "name": "Ada Lovelace",
  "card_status": "active",
  "fines_cents": 0,
  "open_loans": 1
}
```

The sandbox accepts one key, `hl_test_sandbox`. It is public on purpose and only works against the sandbox.

Keep a real key out of source code, URLs, and logs. Anyone who holds it can lend and return books as your library.

## When the key is missing or wrong

A request with no `Authorization` header, or one that does not start with `Bearer`, gets `401` and the code [`unauthorized`](errors.md#unauthorized) (the header is missing, or it does not start with `Bearer`):

```bash
curl "http://127.0.0.1:8080/v1/members/mem_ada"
```

```json
{
  "error": {
    "status": 401,
    "code": "unauthorized",
    "message": "Send your API key as: Authorization: Bearer YOUR_KEY.",
    "doc_url": "https://docs.harborlibrary.example/errors#unauthorized",
    "request_id": "req_000002"
  }
}
```

A request with a key the API does not recognize also gets `401`, with the code [`invalid_api_key`](errors.md#invalid_api_key):

```bash
curl "http://127.0.0.1:8080/v1/members/mem_ada" \
  -H "Authorization: Bearer hl_test_wrong"
```

```json
{
  "error": {
    "status": 401,
    "code": "invalid_api_key",
    "message": "That API key is not recognized.",
    "doc_url": "https://docs.harborlibrary.example/errors#invalid_api_key",
    "request_id": "req_000003"
  }
}
```

Fix: check that the header starts with `Bearer `, and that the key is copied whole, with no spaces or line breaks. Do not retry a `401` unchanged.

## Next

[Pagination](pagination.md), or the [quickstart](quickstart.md) if you have not run it yet.
