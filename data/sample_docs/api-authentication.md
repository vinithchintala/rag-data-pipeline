# Flowstack API Authentication

The Flowstack REST API uses HTTPS for all requests. The base URL is `https://api.flowstack.example/v1`. Every request must be authenticated; unauthenticated requests return `401 Unauthorized`.

## API Keys

The simplest way to authenticate is with an API key. Generate keys from **Settings → Developer → API Keys**. Keys start with the prefix `sk_live_` for production and `sk_test_` for sandbox use.

Pass the key in the `Authorization` header:

```
Authorization: Bearer sk_live_4f8a2b...
```

Treat API keys like passwords. Never expose them in client-side code or public repositories. If a key is compromised, revoke it immediately from the dashboard and generate a new one — revocation takes effect within 60 seconds.

## Rotating API Keys

We recommend rotating API keys every 90 days. To rotate without downtime:

1. Generate a new key in the dashboard.
2. Deploy your services with the new key alongside the old one.
3. Verify traffic is succeeding on the new key.
4. Revoke the old key.

Keys show a "last used" timestamp so you can confirm the old key has stopped receiving traffic before revoking it.

## OAuth 2.0

For integrations acting on behalf of Flowstack users, use OAuth 2.0 with the authorization code flow. Register your application to receive a client ID and secret, then direct users to `https://app.flowstack.example/oauth/authorize`. Request only the scopes you need: `workflows:read`, `workflows:write`, `runs:read`, and `admin` are the available scopes. Refresh tokens are valid for 30 days.

## Rate Limits

API requests are rate limited to **1,000 requests per minute per API key**, with burst capacity up to 1,200. Rate limit status is returned in the `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset` response headers. If you exceed the limit you will receive `429 Too Many Requests`; back off exponentially and retry. Need a higher limit? Growth plans can request up to 5,000 requests per minute from the support team, and Enterprise plans have custom limits.
