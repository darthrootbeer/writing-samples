# Idempotency

**Written for** a developer whose code might send the same "lend a book" request twice, **to** make sure a retry can never lend a book twice.

Networks fail. If your request times out, you do not know whether the library received it. If you send it again and it did, the member has two loans for one request.

The fix is the `Idempotency-Key` header on `POST /v1/loans`. Pick a unique string for each lend you intend to make, and send it again unchanged on every retry of that same lend.

## How it works

- **First request with a key:** the loan is created and the response is stored under the key.
- **Same key, same body:** you get the first response back with status `201`, and the extra header `Idempotent-Replay: true`. No second loan is made. "Same body" means the same JSON content. Key order and spacing do not matter. The response shows the loan as it was when it was created, even if the book has been returned since.
- **Same key, different body:** you get `409` with the code [`idempotency_key_reused`](errors.md#idempotency_key_reused). This usually means your code reused a key by mistake. Use a new key.
- **Failed request:** only successful lends are stored. If a request fails, for example with `book_unavailable`, fix the problem and retry with the same key. It is treated as a first request.
- **Length:** 1 to 64 characters. A longer key returns `400` with the code [`invalid_request`](errors.md#invalid_request).
- **How long keys last:** 24 hours. After that, the same key starts a new lend. The sandbox does not expire keys. It forgets them when you restart it.

## Try it

Lend a book with a key:

```bash
curl -X POST "http://127.0.0.1:8080/v1/loans" \
  -H "Authorization: Bearer hl_test_sandbox" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: ada-bk004-2026-10-26" \
  -d '{"member_id": "mem_ada", "book_id": "bk_004"}'
```

```json
{
  "id": "loan_0005",
  "member_id": "mem_ada",
  "book_id": "bk_004",
  "status": "active",
  "borrowed_on": "2026-10-26",
  "due_on": "2026-11-16",
  "returned_on": null,
  "renewals": 0
}
```

Send the identical request again. The loan is the same, and `bk_004` is not lent a second time. The body is identical, so the proof is in the headers. Add `-i` to the command and you will see these two lines among them:

```text
Idempotent-Replay: true
Location: /v1/loans/loan_0005
```

The command:

```bash
curl -X POST "http://127.0.0.1:8080/v1/loans" \
  -H "Authorization: Bearer hl_test_sandbox" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: ada-bk004-2026-10-26" \
  -d '{"member_id": "mem_ada", "book_id": "bk_004"}'
```

```json
{
  "id": "loan_0005",
  "member_id": "mem_ada",
  "book_id": "bk_004",
  "status": "active",
  "borrowed_on": "2026-10-26",
  "due_on": "2026-11-16",
  "returned_on": null,
  "renewals": 0
}
```

Now reuse the key for a different lend:

```bash
curl -X POST "http://127.0.0.1:8080/v1/loans" \
  -H "Authorization: Bearer hl_test_sandbox" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: ada-bk004-2026-10-26" \
  -d '{"member_id": "mem_grace", "book_id": "bk_003"}'
```

```json
{
  "error": {
    "status": 409,
    "code": "idempotency_key_reused",
    "message": "That Idempotency-Key was already used with a different request. Use a new key.",
    "param": "Idempotency-Key",
    "doc_url": "https://docs.harborlibrary.example/errors#idempotency_key_reused",
    "request_id": "req_000003"
  }
}
```

## The other loan endpoints

- **Return** does no harm if you repeat it. The second call changes nothing and gets `409` with [`loan_not_active`](errors.md#loan_not_active), which means the book was already returned. If you were returning the book, treat that `409` as success.
- **Renew is not safe to repeat.** Each call adds 14 days, up to two renewals. If a renew times out, read the loan with `GET /v1/loans/{loan_id}` and check `renewals` before you try again.

## Next

[Errors](errors.md), then the [loans reference](reference/loans.md).
