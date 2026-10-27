# Members

**Written for** a developer who needs to check a library card before lending, **to** read a member and know whether they can borrow.

A member is a person with a library card.

## The member object

| Field | Type | Meaning |
|---|---|---|
| `id` | string | The member's id, such as `mem_ada`. |
| `name` | string | The member's name. |
| `card_status` | string | `active`, or `blocked` when the member owes more than $10.00 in fines. It turns `active` again when fines are $10.00 or less. A blocked member cannot borrow. |
| `fines_cents` | integer | Fines owed, in cents. 1240 means $12.40. |
| `open_loans` | integer | How many loans are active or overdue. |

This API only reports fines. It does not charge them or set the amount. The front desk does that.

## Get a member

`GET /v1/members/{member_id}`

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

Check `card_status` before you offer to lend a book. Here is a member whose card is blocked:

```bash
curl "http://127.0.0.1:8080/v1/members/mem_rip" \
  -H "Authorization: Bearer hl_test_sandbox"
```

```json
{
  "id": "mem_rip",
  "name": "Rip Van Winkle",
  "card_status": "blocked",
  "fines_cents": 124000,
  "open_loans": 1
}
```

`fines_cents` is 124000, which is $1,240.00. If you try to lend this member a book anyway, the lend fails with [`member_blocked`](../errors.md#member_blocked). The errors page says what to tell the member.

## Errors for this endpoint

| Status | Code | Cause |
|---|---|---|
| 404 | [`member_not_found`](../errors.md#member_not_found) | No member has that id. |

Authentication and rate-limit errors can happen on any request. See [errors](../errors.md).

## Next

[Lend a book](loans.md) to an active member.
