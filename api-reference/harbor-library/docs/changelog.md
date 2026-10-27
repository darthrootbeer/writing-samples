# Changelog

**Written for** a developer who needs to know whether an update can break their code, **to** read what changed and when.

Changes to the Harbor Library Lending API, newest first.

## How versions work

The `v1` at the start of every path is the **major version**. A change that could break existing code, such as removing a field or changing what a status code means, gets a new major version at a new path, such as `/v2`. Adding a field or an endpoint does not. Your code should ignore fields it does not know.

When a new major version ships, the old one keeps working for at least 12 months. The release is announced here first. The version number in this file follows [semantic versioning](https://semver.org).

## 1.0.0 (2026-10-26)

First release. Books, members, and loans. Cursor pagination. Idempotent loan creation. Error codes and rate limits as documented here.
