# Flowstack Integrations

Flowstack connects with the tools your team already uses. Integrations are configured per workspace from the **Integrations** page, and most use OAuth so you never paste credentials into Flowstack.

## Slack

Post workflow results, alerts, and approvals directly to Slack channels. After connecting, use the "Send Slack message" action in any workflow, choosing a channel and message template. You can also trigger workflows from Slack with slash commands — type `/flowstack run "Nightly ETL sync"` to start a run without opening the app. Interactive approval buttons let managers approve or reject requests right from Slack.

## Microsoft Teams

Similar to Slack: send adaptive card notifications to Teams channels and trigger workflow runs from Teams messages. The Teams integration supports posting to private channels and @-mentioning users when a run fails.

## Jira

Automatically create, update, and transition Jira issues from workflows. A common pattern: when a `workflow.run.failed` event fires, create a Jira ticket in your on-call project with the error details and link back to the failed run. The Jira integration supports JQL-based issue search as a workflow step input.

## GitHub

Connect GitHub to trigger workflows on repository events: pushes, pull request opens, release publishes, and workflow (Actions) completions. For example, run your staging deploy workflow when a release is published, then post the result back to the PR as a comment. The GitHub integration uses a GitHub App installed on selected repositories, so permissions stay scoped to exactly what you approve.

## Managing Integrations

Workspace Admins can view, reconnect, or revoke any integration from the Integrations page. Revoking an integration immediately stops all workflows that depend on it; affected workflows are paused and their owners are notified by email so nothing fails silently.
