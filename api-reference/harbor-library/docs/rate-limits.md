# Rate limits

**Written for** a developer whose code calls the API in a loop, **to** stay under the limit and recover correctly when you go over.

Each API key can make 60 requests per minute. Every response says where you stand, in headers:

| Header | Meaning |
|---|---|
| `X-RateLimit-Limit` | Requests allowed per minute. Always 60. |
| `X-RateLimit-Remaining` | Requests you have left in this minute. The sandbox reports 59 on every response except a forced `429`, because it does not keep count. |
| `Retry-After` | Only on a `429`. Seconds to wait before trying again. |

Go over the limit and the API answers `429 Too Many Requests` with the code [`shush`](errors.md#shush), and keeps answering that way until the minute is up.

## See the 429 in the sandbox

You would need to send 61 requests to hit the limit, and the sandbox does not count. To see the response without that, add the header `X-Sandbox-Force: rate_limited`. The sandbox then answers `429`, with `Retry-After: 3` and `X-RateLimit-Remaining: 0`:

```bash
curl "http://127.0.0.1:8080/v1/books" \
  -H "Authorization: Bearer hl_test_sandbox" \
  -H "X-Sandbox-Force: rate_limited"
```

```json
{
  "error": {
    "status": 429,
    "code": "shush",
    "message": "Shh. This is a library. Wait a moment, then try again.",
    "doc_url": "https://docs.harborlibrary.example/errors#shush",
    "request_id": "req_000001"
  }
}
```

## What your code should do

1. On a `429`, wait the number of seconds in `Retry-After`. Do not retry sooner.
2. Then retry the same request. For `POST /v1/loans`, send the same `Idempotency-Key` so the retry cannot lend the book twice.
3. If you get `429` again, double your last wait. For example, wait 3 seconds, then 6, then 12. Stop after five tries and tell the user.
4. To stay under the limit, list with a large `limit` (up to 100) instead of fetching items one at a time.

The `message` on a `429` is a joke for developers. Do not show it to a library patron. Show your own text, such as "The system is busy. Please try again in a moment."

## Next

[Errors](errors.md) for every other code.
