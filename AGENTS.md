# AGENTS

## Project
kaufland is a Python wrapper for the Kaufland Marketplace Seller API. It should mirror the architecture and public surface of `python-amazon-sp-api`, especially the `sp_api.base` package.

## Scope (Current)
Only implement the base client (sync + asyncio) and shared primitives (request signing, auth headers, HTTP transport, response object, exceptions). Do not add service-specific endpoints yet.

## References
Use `swagger.json` and the official Kaufland docs for endpoints/headers. The PHP examples in the task description are the canonical signing reference.

## Signing
- Base URL: `https://sellerapi.kaufland.com/v2`
- Signature is HMAC-SHA256 of the string:
  `<METHOD>\n<URI>\n<BODY>\n<TIMESTAMP>`
- `URI` is the full URL including query string.
- `BODY` is the raw JSON string for POST/PATCH/PUT; empty string for GET/DELETE.
- `TIMESTAMP` is Unix seconds.
- Required headers:
  `Accept: application/json`
  `Content-Type: application/json` when body present
  `Shop-Client-Key`, `Shop-Timestamp`, `Shop-Signature`, `User-Agent`
- Signature encoding is configurable (`hex` default, `base64` optional).
- Partner credentials (if provided) must add:
  `Shop-Partner-Client-Key`, `Shop-Partner-Signature`

## Layout
- Sync code lives in `kaufland/` and async code lives in `kaufland/asyncio/`.
- Provide the same public API surface in sync and async.
- Client modules are generated from `swagger.json` via `tools/generate_clients.py`.
- Keep shared logic (signing, header building, response parsing, error mapping) in a common module to avoid drift.
- Match `python-amazon-sp-api` naming and structure as closely as practical (e.g., BaseClient, ApiResponse, exceptions, credentials/session handling).

## Quality Bar
- No hardcoded credentials; read from env or passed in constructor.
- Deterministic request signing and header formation.
- Minimal tests for signing and header generation (pure unit tests).
