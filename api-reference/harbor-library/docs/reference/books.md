# Books

**Written for** a developer who needs to search the catalog or check whether a copy is on the shelf, **to** call the two book endpoints and read their results.

A book is a title the library owns. It can have many copies.

## The book object

| Field | Type | Meaning |
|---|---|---|
| `id` | string | The book's id, such as `bk_042`. |
| `title` | string | The title. |
| `author` | string | The author. |
| `copies_total` | integer | How many copies the library owns. |
| `copies_available` | integer | How many copies are on the shelf right now. |

## List books

`GET /v1/books`

Returns books one page at a time. See [pagination](../pagination.md).

| Query parameter | Type | Meaning |
|---|---|---|
| `q` | string | Text to find in the title or the author. Not case sensitive. |
| `available` | boolean | `true` returns only books with `copies_available` above 0. `false` or leaving it out returns all books. Any other value returns `400`. |
| `limit`, `cursor` | | See [pagination](../pagination.md). |

```bash
curl "http://127.0.0.1:8080/v1/books?q=earthsea" \
  -H "Authorization: Bearer hl_test_sandbox"
```

```json
{
  "data": [
    {
      "id": "bk_002",
      "title": "A Wizard of Earthsea",
      "author": "Ursula K. Le Guin",
      "copies_total": 1,
      "copies_available": 0
    }
  ],
  "has_more": false,
  "next_cursor": null
}
```

## Get a book

`GET /v1/books/{book_id}`

```bash
curl "http://127.0.0.1:8080/v1/books/bk_004" \
  -H "Authorization: Bearer hl_test_sandbox"
```

```json
{
  "id": "bk_004",
  "title": "Kindred",
  "author": "Octavia E. Butler",
  "copies_total": 1,
  "copies_available": 1
}
```

If no book has that id, you get `404` with the code [`book_not_found`](../errors.md#book_not_found):

```bash
curl "http://127.0.0.1:8080/v1/books/bk_999" \
  -H "Authorization: Bearer hl_test_sandbox"
```

```json
{
  "error": {
    "status": 404,
    "code": "book_not_found",
    "message": "No book has the id bk_999.",
    "param": "book_id",
    "doc_url": "https://docs.harborlibrary.example/errors#book_not_found",
    "request_id": "req_000003"
  }
}
```

## Errors for these endpoints

| Status | Code | Cause |
|---|---|---|
| 400 | [`invalid_request`](../errors.md#invalid_request) | `limit` is out of range, or `available` is not `true` or `false`. |
| 400 | [`invalid_cursor`](../errors.md#invalid_cursor) | The `cursor` is not one the API gave you. |
| 404 | [`book_not_found`](../errors.md#book_not_found) | No book has that id. |

Authentication and rate-limit errors can happen on any request. See [errors](../errors.md).

## Next

[Lend a book](loans.md) to a member, or check the [member](members.md) first.
