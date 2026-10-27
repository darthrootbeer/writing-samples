# Loans

**Written for** a developer building the lend, renew, and return screens of a library app, **to** call each loan endpoint and handle every way it can fail.

A loan is one copy of a book lent to one member.

Examples on this page assume a fresh sandbox, so ids such as `loan_0005` may differ from the ones in the [quickstart](../quickstart.md), which lends a different book.

## The loan object

| Field | Type | Meaning |
|---|---|---|
| `id` | string | The loan's id, such as `loan_0002`. |
| `member_id` | string | Who has the book. |
| `book_id` | string | Which book. |
| `status` | string | `active`, `overdue`, or `returned`. A loan turns `overdue` the day after `due_on`. |
| `borrowed_on` | date | The day the book was lent, as `YYYY-MM-DD`. |
| `due_on` | date | The day the book is due back. |
| `returned_on` | date or null | The day it came back. `null` until then. |
| `renewals` | integer | How many times the loan has been renewed, from 0 to 2. |

## List loans

`GET /v1/loans`

| Query parameter | Type | Meaning |
|---|---|---|
| `member_id` | string | Return only this member's loans. |
| `status` | string | `active`, `overdue`, or `returned`. Any other value returns `400` with the code [`invalid_request`](../errors.md#invalid_request). |
| `limit`, `cursor` | | See [pagination](../pagination.md). |

Find everything Ada Lovelace has not returned yet:

```bash
curl "http://127.0.0.1:8080/v1/loans?member_id=mem_ada&status=active" \
  -H "Authorization: Bearer hl_test_sandbox"
```

```json
{
  "data": [
    {
      "id": "loan_0002",
      "member_id": "mem_ada",
      "book_id": "bk_002",
      "status": "active",
      "borrowed_on": "2026-10-12",
      "due_on": "2026-11-02",
      "returned_on": null,
      "renewals": 0
    }
  ],
  "has_more": false,
  "next_cursor": null
}
```

**Errors for list and get**

| Status | Code | Cause |
|---|---|---|
| 400 | [`invalid_request`](../errors.md#invalid_request) | `limit` is out of range, or `status` is not one of the three values. |
| 400 | [`invalid_cursor`](../errors.md#invalid_cursor) | The `cursor` is not one the API gave you. |
| 404 | [`loan_not_found`](../errors.md#loan_not_found) | No loan has that id (get only). |

Authentication and rate-limit errors can happen on any request. See [errors](../errors.md).

## Get a loan

`GET /v1/loans/{loan_id}`

```bash
curl "http://127.0.0.1:8080/v1/loans/loan_0004" \
  -H "Authorization: Bearer hl_test_sandbox"
```

```json
{
  "id": "loan_0004",
  "member_id": "mem_grace",
  "book_id": "bk_004",
  "status": "overdue",
  "borrowed_on": "2026-09-30",
  "due_on": "2026-10-21",
  "returned_on": null,
  "renewals": 2
}
```

This loan was due on 2026-10-21. The sandbox's "today" is 2026-10-26, so its status is `overdue`.

## Lend a book

`POST /v1/loans`

Lends one copy of a book to a member for 21 days.

| Body field | Type | Meaning |
|---|---|---|
| `member_id` | string, required | Who is borrowing. |
| `book_id` | string, required | Which book. |

Send `Content-Type: application/json`. The sandbox accepts other types, but the real API will not.

| Header | Meaning |
|---|---|
| `Idempotency-Key` | Send one on every lend. A unique string, 1 to 64 characters. It makes a retry safe. See [idempotency](../idempotency.md). |

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

`bk_004` had one copy. Now it has none, so the next request for it fails:

```bash
curl -X POST "http://127.0.0.1:8080/v1/loans" \
  -H "Authorization: Bearer hl_test_sandbox" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: grace-bk004-2026-10-26" \
  -d '{"member_id": "mem_grace", "book_id": "bk_004"}'
```

```json
{
  "error": {
    "status": 409,
    "code": "book_unavailable",
    "message": "All copies of \"Kindred\" are on loan.",
    "param": "book_id",
    "doc_url": "https://docs.harborlibrary.example/errors#book_unavailable",
    "request_id": "req_000004"
  }
}
```

Because the lend failed, nothing was stored under that key. You can retry it with the same key once a copy is returned.

**Errors for this endpoint**

| Status | Code | Cause |
|---|---|---|
| 400 | [`invalid_request`](../errors.md#invalid_request) | `member_id` or `book_id` is missing or not a string, or the `Idempotency-Key` is not 1 to 64 characters. |
| 400 | [`invalid_json`](../errors.md#invalid_json) | The body is not a JSON object. |
| 403 | [`member_blocked`](../errors.md#member_blocked) | The member owes more than $10.00 in fines. |
| 404 | [`member_not_found`](../errors.md#member_not_found), [`book_not_found`](../errors.md#book_not_found) | The id does not exist. |
| 409 | [`book_unavailable`](../errors.md#book_unavailable) | Every copy is on loan. |
| 409 | [`idempotency_key_reused`](../errors.md#idempotency_key_reused) | The key was already used for a different lend. |

If more than one of these applies, the API reports the first one in the order [the errors page](../errors.md#when-more-than-one-error-applies) gives.

## Renew a loan

`POST /v1/loans/{loan_id}/renew`

Adds 14 days to the due date. A loan can be renewed twice. An overdue loan cannot be renewed. Renewing is not safe to repeat: each call adds 14 days. Renew ignores any request body. See [idempotency](../idempotency.md#the-other-loan-endpoints).

```bash
curl -X POST "http://127.0.0.1:8080/v1/loans/loan_0002/renew" \
  -H "Authorization: Bearer hl_test_sandbox"
```

```json
{
  "id": "loan_0002",
  "member_id": "mem_ada",
  "book_id": "bk_002",
  "status": "active",
  "borrowed_on": "2026-10-12",
  "due_on": "2026-11-16",
  "returned_on": null,
  "renewals": 1
}
```

`due_on` moved from 2026-11-02 to 2026-11-16, and `renewals` is now 1.

**Errors for this endpoint**

| Status | Code | Cause |
|---|---|---|
| 404 | [`loan_not_found`](../errors.md#loan_not_found) | The id does not exist. |
| 409 | [`loan_not_active`](../errors.md#loan_not_active) | The book was already returned. |
| 409 | [`loan_overdue`](../errors.md#loan_overdue) | The loan is past due. Return the book first. |
| 409 | [`renewal_limit_reached`](../errors.md#renewal_limit_reached) | The loan was already renewed twice. |

An overdue loan fails like this:

```bash
curl -X POST "http://127.0.0.1:8080/v1/loans/loan_0004/renew" \
  -H "Authorization: Bearer hl_test_sandbox"
```

```json
{
  "error": {
    "status": 409,
    "code": "loan_overdue",
    "message": "loan_0004 is overdue. Return the book first. An overdue loan cannot be renewed.",
    "param": "loan_id",
    "doc_url": "https://docs.harborlibrary.example/errors#loan_overdue",
    "request_id": "req_000006"
  }
}
```

## Return a book

`POST /v1/loans/{loan_id}/return`

Marks the loan returned and puts the copy back on the shelf. Returning twice does no harm: the second call changes nothing and returns `409` `loan_not_active`, which means the book was already returned. Treat that `409` as success.

```bash
curl -X POST "http://127.0.0.1:8080/v1/loans/loan_0004/return" \
  -H "Authorization: Bearer hl_test_sandbox"
```

```json
{
  "id": "loan_0004",
  "member_id": "mem_grace",
  "book_id": "bk_004",
  "status": "returned",
  "borrowed_on": "2026-09-30",
  "due_on": "2026-10-21",
  "returned_on": "2026-10-26",
  "renewals": 2
}
```

**Errors for this endpoint**

| Status | Code | Cause |
|---|---|---|
| 404 | [`loan_not_found`](../errors.md#loan_not_found) | The id does not exist. |
| 409 | [`loan_not_active`](../errors.md#loan_not_active) | The book was already returned. |

Returning the same loan twice fails the second time:

```bash
curl -X POST "http://127.0.0.1:8080/v1/loans/loan_0004/return" \
  -H "Authorization: Bearer hl_test_sandbox"
```

```json
{
  "error": {
    "status": 409,
    "code": "loan_not_active",
    "message": "loan_0004 was already returned on 2026-10-26.",
    "param": "loan_id",
    "doc_url": "https://docs.harborlibrary.example/errors#loan_not_active",
    "request_id": "req_000008"
  }
}
```

## Next

Something failed? Read [errors](../errors.md). Building the lend screen? Read [idempotency](../idempotency.md).
