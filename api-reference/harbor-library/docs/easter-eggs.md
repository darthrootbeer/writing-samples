# Easter eggs

**Written for** anyone who found a strange response in the sandbox, **to** confirm it is a joke on purpose and not a bug.

The sandbox has a few jokes. They are real, they are stable, and they are listed here. None of them can happen by accident.

## Ask for coffee

`GET /v1/teapot` needs no API key and always returns `418`. Other methods on that path return `405`, with or without a key. The status comes from [RFC 2324](https://www.rfc-editor.org/rfc/rfc2324), the Hyper Text Coffee Pot Control Protocol, an April Fools' joke from 1998 that web servers have kept ever since.

```bash
curl "http://127.0.0.1:8080/v1/teapot"
```

```json
{
  "error": {
    "status": 418,
    "code": "teapot",
    "message": "I'm a teapot, short and stout. The library does not brew coffee.",
    "doc_url": "https://docs.harborlibrary.example/errors#teapot",
    "request_id": "req_000001"
  }
}
```

## The answer

Book `bk_042` is *The Hitchhiker's Guide to the Galaxy*. The library owns 42 copies:

```bash
curl "http://127.0.0.1:8080/v1/books/bk_042" \
  -H "Authorization: Bearer hl_test_sandbox"
```

```json
{
  "id": "bk_042",
  "title": "The Hitchhiker's Guide to the Galaxy",
  "author": "Douglas Adams",
  "copies_total": 42,
  "copies_available": 42
}
```

## Quiet, please

The rate limit error is called [`shush`](errors.md#shush), and its message asks you to be quiet. See [rate limits](rate-limits.md).

## Rip Van Winkle

Member `mem_rip` borrowed *Frankenstein* on 2006-03-14 and has not returned it. His fines are $1,240.00, so his card is blocked. See [members](reference/members.md) and the [`member_blocked`](errors.md#member_blocked) error.

## The librarian

Every response carries the header `X-Librarian: Marian`. Check with `curl -i`. It is a nod to the librarian in *The Music Man*.

## Next

[Back to the quickstart](quickstart.md).
