# Quickstart: lend your first book

**Written for** a developer building a self-checkout kiosk or a library app, **to** lend a book, check the loan, and return it in about five minutes.

You need Python 3.10 or newer and `curl`. You do not need an account. The sandbox answers the same requests as the real API, with a small set of sample books and members.

You will use two terminal windows: one for the sandbox, which stays running, and one for the `curl` commands.

## 1. Start the sandbox

In the first terminal, go to the root of the `writing-samples` repository (the folder that contains `api-reference`) and run:

```bash
python3 api-reference/harbor-library/mock/server.py
```

You should see this one line, and then nothing more. That means it is running:

```text
Harbor Library sandbox on http://127.0.0.1:8080  (API key: hl_test_sandbox)
```

Leave this window open. If you see `Address already in use`, something else is using port 8080. Add a different port to the end of the command, such as `... server.py 8090`, and use that port in place of 8080 in every example.

Every example in these docs uses `http://127.0.0.1:8080`. The real API would use `https://api.harborlibrary.example` instead, and everything else would stay the same. The `v1` in each path is the major version. [The changelog](changelog.md#how-versions-work) explains it.

## 2. Find a book you can borrow

Open the second terminal for the rest of this page.

Every request needs your API key in an `Authorization` header. The word `Bearer` means "whoever carries this key is allowed in." The sandbox key is `hl_test_sandbox`.

Search for books by Ursula K. Le Guin that have a copy on the shelf:

```bash
curl "http://127.0.0.1:8080/v1/books?q=guin&available=true" \
  -H "Authorization: Bearer hl_test_sandbox"
```

```json
{
  "data": [
    {
      "id": "bk_003",
      "title": "The Left Hand of Darkness",
      "author": "Ursula K. Le Guin",
      "copies_total": 3,
      "copies_available": 3
    }
  ],
  "has_more": false,
  "next_cursor": null
}
```

One book comes back, `bk_003`. The other Le Guin book in the sandbox, `bk_002`, is checked out, so the filter leaves it out. The `has_more` and `next_cursor` fields tell you whether there are more pages of results. Here there are not. [Pagination](pagination.md) explains them.

## 3. Lend it

Lend `bk_003` to the member `mem_grace`. The `Idempotency-Key` header makes the request safe to retry: if your network drops and you send the same request again with the same key, you get the same loan back and the book is not lent twice. [Idempotency](idempotency.md) has the details.

```bash
curl -X POST "http://127.0.0.1:8080/v1/loans" \
  -H "Authorization: Bearer hl_test_sandbox" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: quickstart-grace-bk003" \
  -d '{"member_id": "mem_grace", "book_id": "bk_003"}'
```

```json
{
  "id": "loan_0005",
  "member_id": "mem_grace",
  "book_id": "bk_003",
  "status": "active",
  "borrowed_on": "2026-10-26",
  "due_on": "2026-11-16",
  "returned_on": null,
  "renewals": 0
}
```

The response status is `201 Created`. Plain `curl` prints only the body. Add `-i` to the command to see the status line. The loan has an `id` and a `due_on` date 21 days from the sandbox's fixed "today", 2026-10-26. Write down the `id`. On a fresh sandbox it is `loan_0005`. If you have run other examples first, yours may differ, so copy it from your own response.

## 4. Return it

Use the loan `id` from the last step in place of `loan_0005`:

```bash
curl -X POST "http://127.0.0.1:8080/v1/loans/loan_0005/return" \
  -H "Authorization: Bearer hl_test_sandbox"
```

```json
{
  "id": "loan_0005",
  "member_id": "mem_grace",
  "book_id": "bk_003",
  "status": "returned",
  "borrowed_on": "2026-10-26",
  "due_on": "2026-11-16",
  "returned_on": "2026-10-26",
  "renewals": 0
}
```

The loan now has `"status": "returned"` and a `returned_on` date. You have lent a book and taken it back.

## Start over

The sandbox keeps its data in memory. To reset it, stop it with `Ctrl+C` in the first terminal and start it again. Each page of these docs assumes a fresh sandbox.

## Next

- Something went wrong? [Errors](errors.md) lists every error code and how to fix it.
- Ready to build? Read [authentication](authentication.md) and [idempotency](idempotency.md), then the [loans reference](reference/loans.md).
- Curious what else the sandbox can do? [Easter eggs](easter-eggs.md).
