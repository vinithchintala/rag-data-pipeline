# Flowstack Webhooks

Webhooks let Flowstack notify your systems in real time when events happen in your workspace. Instead of polling the API, register an HTTPS endpoint and we will POST a JSON payload to it whenever a subscribed event occurs.

## Supported Events

- `workflow.created` — a new workflow is saved.
- `workflow.run.started` — a workflow run begins execution.
- `workflow.run.completed` — a workflow run finishes successfully.
- `workflow.run.failed` — a workflow run fails or times out. The payload includes the error message and the failed step name.
- `user.invited` — a new user is invited to the workspace.
- `billing.plan_changed` — the workspace plan is upgraded or downgraded.

Subscribe to events from **Settings → Developer → Webhooks**. You can register up to 20 endpoints per workspace.

## Payload Example

```json
{
  "id": "evt_9d31ab77",
  "type": "workflow.run.failed",
  "created_at": "2026-09-14T18:22:05Z",
  "workspace_id": "ws_42",
  "data": {
    "workflow_id": "wf_108",
    "workflow_name": "Nightly ETL sync",
    "run_id": "run_55120",
    "failed_step": "load_to_warehouse",
    "error": "Connection timed out after 30s"
  }
}
```

## Verifying Signatures

Every webhook request includes an `X-Flowstack-Signature` header containing an HMAC-SHA256 of the raw request body, computed with your endpoint's signing secret. Always verify the signature before acting on a payload to ensure the request genuinely came from Flowstack.

## Retries

If your endpoint does not respond with a 2xx status within 10 seconds, we retry delivery with exponential backoff: after 1 minute, 5 minutes, 30 minutes, 2 hours, and 8 hours. After 5 failed attempts the event is moved to a dead-letter queue, visible in the dashboard for 7 days, where you can manually replay it. Endpoints that fail more than 100 deliveries in 24 hours are automatically disabled and the workspace owner is notified by email.
