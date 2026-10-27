# Errors

**Written for** a developer who just got an error, or a support engineer helping a customer who did, **to** find the code, learn the cause, and know exactly what to do next.

When a request fails, the HTTP status tells you the kind of failure, and the body tells you exactly what happened. Every error has the same shape:

```bash
curl -X POST "http://127.0.0.1:8080/v1/loans" \
  -H "Authorization: Bearer hl_test_sandbox" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: rip-bk003-2026-10-26" \
  -d '{"member_id": "mem_rip", "book_id": "bk_003"}'
```

```json
{
  "error": {
    "status": 403,
    "code": "member_blocked",
    "message": "Rip Van Winkle owes $1,240.00 in fines. A card with more than $10.00 in fines is blocked.",
    "param": "member_id",
    "doc_url": "https://docs.harborlibrary.example/errors#member_blocked",
    "request_id": "req_000001"
  }
}
```

| Field | Meaning |
|---|---|
| `status` | The HTTP status, repeated so you can log the body alone. |
| `code` | A short, stable name for the problem. Write your `if` statements on this. It will not change. |
| `message` | A sentence for a developer. It can change, so do not match on it, and do not show it to a library patron as it is. |
| `param` | The input that caused the error. Only present when there is one. |
| `doc_url` | The section of this page that explains the code. |
| `request_id` | Quote this when you contact support. Every response also has it in the `X-Request-Id` header. |

## What to do with each status

- **4xx** means the request needs a change. Do not retry it unchanged. Three codes can succeed later with no change to the request: [`shush`](#shush) after a wait, [`book_unavailable`](#book_unavailable) after a return, and [`member_blocked`](#member_blocked) after the fines are paid.

A **patron** is a library member, the person standing at the desk. The "Tell the patron" lines below are suggested words for them.
- **429** means slow down. Wait, then retry. See [rate limits](rate-limits.md).
- **5xx** means the library's system had a problem. Retry with the same `Idempotency-Key`. See [5xx errors](#5xx-errors).

## Contacting support

If you cannot solve it with this page, send the developer desk these four things:

1. The `request_id` from the error body, or the `X-Request-Id` header.
2. The time of the request, with the time zone.
3. The method and path, such as `POST /v1/loans`.
4. The error `code`.

The desk is at `https://docs.harborlibrary.example/support`. Never send your API key.

## When more than one error applies

The API checks in a fixed order and reports the first problem it finds.

**Every request:** the API key comes first, so a bad key beats every other error. Then the path and method (`route_not_found`, `method_not_allowed`). The one exception is `GET /v1/teapot`, which needs no key.

**Lend (`POST /v1/loans`), after the key and path:** the body is valid JSON (`invalid_json`), then `member_id` and `book_id` are present and are strings (`invalid_request`), then the `Idempotency-Key` is 1 to 64 characters (`invalid_request`), then the key was not used for a different lend (`idempotency_key_reused`), then the member exists, then the book exists, then the member is not blocked, then a copy is available.

**Renew, after the key and path:** the loan exists, then it is not already returned, then it is not overdue, then it has renewals left. So an overdue loan that has used both renewals reports `loan_overdue`.

**Return, after the key and path:** the loan exists, then it is not already returned.

Renew and return ignore any request body.

## 400 errors

### `invalid_request`

- **Cause:** A parameter is missing, the wrong type, or out of range. The `param` field names it.
- **Fix:** Correct that parameter and send the request again.
- **Retry?** Not unchanged.

### `invalid_json`

- **Cause:** The body is not valid JSON, or it is not a JSON object.
- **Fix:** Check for a trailing comma or a missing quote.
- **Retry?** Not unchanged.

### `invalid_cursor`

- **Cause:** The `cursor` is not one the API gave you.
- **Fix:** Start again from the first page. See [pagination](pagination.md).
- **Retry?** Not unchanged.

## 401 errors

### `unauthorized`

- **Cause:** There is no `Authorization` header, or it does not start with `Bearer`.
- **Fix:** Add it. See [authentication](authentication.md).
- **Retry?** Not unchanged.

### `invalid_api_key`

- **Cause:** The key is not recognized.
- **Fix:** Copy the key again, with no spaces or line breaks.
- **Retry?** Not unchanged.

## 403 errors

### `member_blocked`

- **Cause:** The member owes more than $10.00 in fines. The amount is `fines_cents` on the [member](reference/members.md).
- **Fix:** The member pays at the front desk. The card works again when fines are $10.00 or less. Then try again.
- **Retry?** Only after the member has paid.
- **Tell the patron:** "Your card has more than $10.00 in fines. Please see the front desk."

## 404 errors

### `book_not_found`

- **Cause:** No book has that id.
- **Fix:** Check the id.
- **Retry?** Not unchanged.
- **Tell the patron:** "We don't have that title in the catalog. Let's search by author."

### `member_not_found`

- **Cause:** No member has that id.
- **Fix:** Check the id.
- **Retry?** Not unchanged.
- **Tell the patron:** "I can't find that library card. Can you read me the number again?"

### `loan_not_found`

- **Cause:** No loan has that id.
- **Fix:** Check the id.
- **Retry?** Not unchanged.

### `route_not_found`

- **Cause:** There is no endpoint at that path.
- **Fix:** Check the path.
- **Retry?** Not unchanged.

## 405 errors

### `method_not_allowed`

- **Cause:** The path exists, but not for that method, such as `DELETE /v1/loans/loan_0002`. The API has no delete.
- **Fix:** Check the method against the [reference](reference/loans.md).
- **Retry?** Not unchanged.

## 409 errors

The request was fine, but the library's records do not allow it right now.

### `book_unavailable`

- **Cause:** Every copy is on loan.
- **Fix:** Offer another book, or check again after a return. A retry with the same `Idempotency-Key` is safe.
- **Retry?** Later, yes.
- **Tell the patron:** "All copies are out right now. Would you like another book?"

### `loan_not_active`

- **Cause:** The book was already returned. This is also what a second `return` on the same loan gets. It means the first one worked.
- **Fix:** Nothing to do. The loan is finished. Treat it as success if you were returning the book.
- **Retry?** No.
- **Tell the patron:** "That book is already checked in."

### `loan_overdue`

- **Cause:** You tried to renew a loan that is past its due date.
- **Fix:** Return the book. An overdue loan cannot be renewed.
- **Fines:** This API does not charge a fine for returning late. Any fine is set by the front desk and appears in `fines_cents` on the member.
- **Retry?** Not until the book is returned and lent again.
- **Tell the patron:** "This book is past due, so it can't be renewed. Please return it at the desk."

### `renewal_limit_reached`

- **Cause:** The loan was already renewed twice.
- **Fix:** The patron returns the book. After that, the same patron may borrow it again if a copy is on the shelf.
- **Retry?** No. Another renew will fail the same way.
- **Tell the patron:** "You've renewed this book twice, which is the limit. Please bring it back, and you can borrow it again if it's on the shelf."

### `idempotency_key_reused`

- **Cause:** The `Idempotency-Key` was already used for a different lend.
- **Fix:** Use a new key for each different lend. Only repeat a key when you are retrying the same lend. See [idempotency](idempotency.md).
- **Retry?** With a new key.

## 418 error

### `teapot`

- **Cause:** You asked the library for coffee at `GET /v1/teapot`.
- **Fix:** Have some tea. See [Easter eggs](easter-eggs.md).
- **Retry?** You will get the same answer.

## 429 error

### `shush`

- **Cause:** More than 60 requests in a minute.
- **Fix:** Wait for the number of seconds in the `Retry-After` header, then retry. See [rate limits](rate-limits.md).
- **Retry?** Yes, after the wait.

## 5xx errors

A `5xx` response is a problem on the library's side, not yours. It has the same shape. The code is `internal_error` for `500` and `unavailable` for `503`.

### `internal_error`

A `500`. Something broke on the library's side. Handle it the way the next section describes.

### `unavailable`

A `503`. The library system is busy or down for a moment. Here is a full example:

```json
{
  "error": {
    "status": 503,
    "code": "unavailable",
    "message": "The library system is busy. Try again in a moment.",
    "doc_url": "https://docs.harborlibrary.example/errors#unavailable",
    "request_id": "req_000207"
  }
}
```

- **Cause:** An outage or a bug on the library's side.
- **Fix:** Wait a few seconds and retry. For `POST /v1/loans`, send the same `Idempotency-Key`, so a lend that did go through is not made twice. **Do not blindly retry a renew.** The first one may have worked, and each renew adds 14 days. Read the loan with `GET /v1/loans/{loan_id}` and check `renewals` first. If it keeps failing, [contact support](#contacting-support) with the `request_id`.
- **Retry?** Yes, with a growing wait, up to five tries. Lend and return are safe to retry. Renew needs the check above.

The sandbox never returns a `5xx`.
