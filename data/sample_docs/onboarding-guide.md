# Flowstack Onboarding Guide

Welcome to Flowstack! This guide walks you through setting up your workspace, inviting your team, and running your first workflow in under 15 minutes.

## Create Your Workspace

Sign up at app.flowstack.example with your work email. You will be prompted to name your workspace — pick something your whole company will recognize, like "Acme Corp". Choose your data region (US or EU) during signup; this determines where your data is stored and cannot be changed later, so choose carefully if you have data residency requirements.

## Invite Your Team

Go to **Settings → Members → Invite**. Enter email addresses separated by commas, or upload a CSV for bulk invites. Assign each person a role:

- **Admin** — full control over billing, members, and workspace settings.
- **Builder** — can create and edit workflows but cannot change billing.
- **Viewer** — read-only access to workflows and run history.

Invited users receive an email and have 7 days to accept before the invite expires. On Growth and Enterprise plans you can also enable SSO so teammates sign in with your identity provider instead of passwords.

## Run Your First Workflow

1. Click **New Workflow** and choose a template — "Daily report email" is a great first pick.
2. Connect your first integration (e.g., Slack or your database) by following the on-screen OAuth prompts.
3. Customize the steps: every workflow is a sequence of triggers, actions, and conditions you can drag to reorder.
4. Click **Test run** to execute once with sample data and inspect the output of each step.
5. Toggle the workflow **On** to activate it on its schedule.

## Templates Gallery

The templates gallery contains 80+ prebuilt workflows for common tasks: syncing CRM data, posting deploy notifications, backing up databases, and triaging support tickets. Templates are free on all plans and can be previewed before installation.
