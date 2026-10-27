# Pagination

**Written for** a developer who needs to read a list that is longer than one response, **to** page through it correctly to the end.

List endpoints return one page at a time. Use `limit` to choose the page size, from 1 to 100. The default is 20.

Every list response has a `data` array and two more fields:

| Field | Meaning |
|---|---|
| `has_more` | `true` if another page exists. |
| `next_cursor` | Pass this value as `cursor` to get the next page. `null` on the last page. |

Ask for two books at a time:

```bash
curl "http://127.0.0.1:8080/v1/books?limit=2" \
  -H "Authorization: Bearer hl_test_sandbox"
```

```json
{
  "data": [
    {
      "id": "bk_001",
      "title": "Frankenstein",
      "author": "Mary Shelley",
      "copies_total": 2,
      "copies_available": 1
    },
    {
      "id": "bk_002",
      "title": "A Wizard of Earthsea",
      "author": "Ursula K. Le Guin",
      "copies_total": 1,
      "copies_available": 0
    }
  ],
  "has_more": true,
  "next_cursor": "cur_2"
}
```

`has_more` is `true`, so ask for the next page. Pass `next_cursor` back exactly as you received it:

```bash
curl "http://127.0.0.1:8080/v1/books?limit=2&cursor=cur_2" \
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
    },
    {
      "id": "bk_004",
      "title": "Kindred",
      "author": "Octavia E. Butler",
      "copies_total": 1,
      "copies_available": 1
    }
  ],
  "has_more": true,
  "next_cursor": "cur_4"
}
```

Keep going until `has_more` is `false`.

## Rules

- Treat a cursor as a sealed envelope. Do not build one, change one, or save one for later. The sandbox cursors look like `cur_2`. The real ones will not, so never depend on the format.
- Send the same filters on every page. A cursor remembers only your place in the list, not your search. If you change `q`, `status`, or any other filter between pages, you get whatever is at that place in the new list, often an empty page. Start again from the first page when you change a filter.
- A cursor that is not in the format the API uses returns `400` with the code [`invalid_cursor`](errors.md#invalid_cursor). A cursor in the right format that points past the end of the list returns an empty page, with `has_more` set to `false`. Either way, start again from the first page.
- A bad `limit`, such as `0` or `500`, returns `400` with the code [`invalid_request`](errors.md#invalid_request).

## Next

[Books](reference/books.md) and [loans](reference/loans.md) are the two lists you can page through.
