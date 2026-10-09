# Exporting Your Data

You own your data. Flowstack provides several ways to export workflows, run history, and audit logs so you can back them up, analyze them elsewhere, or meet compliance requirements.

## Manual Export

From any workflow page, click the **⋯ menu → Export**. You can download:

- **Workflow definition** as JSON — the full step configuration, reusable for backup or migration.
- **Run history** as CSV — one row per run with timestamps, status, duration, and per-step outcomes.
- **Audit log** as CSV — available to Admins on Growth and Enterprise plans.

Manual exports are generated on demand and download directly in your browser. Exports are limited to 500,000 rows per file; larger histories should use the bulk API below.

## Bulk Export API

For programmatic access, use the bulk export endpoints:

```
GET /v1/exports/runs?from=2026-01-01&to=2026-03-31&format=jsonl
```

Exports run asynchronously. The API returns an export job ID; poll `GET /v1/exports/{id}` until the status is `ready`, then download the file from the provided URL. Download links expire after 7 days. Supported formats are CSV, JSON, and JSONL. Bulk export is rate limited to 10 concurrent jobs per workspace.

## Scheduled Exports

Growth and Enterprise workspaces can schedule recurring exports to their own cloud storage. Configure a destination (Amazon S3, Google Cloud Storage, or Azure Blob Storage) under **Settings → Data → Scheduled Exports**, choose daily or weekly cadence, and Flowstack will deliver encrypted export files automatically. This is the recommended approach for compliance archiving.

## Export Retention

Generated export files are stored for 30 days and then deleted automatically. If you need exports retained longer, use scheduled exports to your own storage bucket, where retention is under your control.
