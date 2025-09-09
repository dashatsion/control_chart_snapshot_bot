
# Control Chart Snapshot Bot (Jira → Slack)

A minimal open‑source bot that computes **QA cycle time** (from `Ready for QA` to `Done`), generates a weekly **Control Chart snapshot** (PNG + stats), and posts it to **Slack**.

> Built for teams that currently do this manually. Plug in Jira + Slack tokens, schedule via GitHub Actions, and you're done.

## What it does
- Pulls Jira issues and parses **status transitions** from changelog
- Computes **QA cycle time** per issue
- Posts weekly stats to Slack: `Mean / Median / P75` and a histogram image
- (Optional) Flags anomalies over a configurable threshold

## Quick start
1. **Clone** this repo and add your secrets in GitHub → *Settings → Secrets and variables → Actions*:

   - `JIRA_BASE_URL` — e.g. `https://your-domain.atlassian.net`
   - `JIRA_EMAIL` — Atlassian account email
   - `JIRA_API_TOKEN` — Jira API token
   - `JIRA_PROJECT_KEYS` — e.g. `PROJ1,PROJ2`
   - `SLACK_BOT_TOKEN` — `xoxb-...`
   - `SLACK_CHANNEL_ID` — channel id like `C0123456789`

2. **Adjust statuses** in workflow env if your team uses custom names (defaults are `Ready for QA` and `Done`).

3. **Run once manually**: GitHub → Actions → *Weekly QA Snapshot* → *Run workflow*.

4. **Cron schedule**: by default runs **Mondays 09:00 America/New_York** (cron is UTC). Adjust if needed.

## Local run (optional)
```bash
pip install -r requirements.txt
cp .env.example .env  # fill it
python -m src.main
```

## Config via `.env`
See `.env.example`. Values from environment variables override defaults in code.

## Notes
- Requires Jira permissions: **Browse projects**, **View issue**, **View change history** (to access changelog).
- If a ticket enters QA multiple times, the bot uses the **first completed QA cycle** by default.
- Extend via `ROADMAP` below.

## Roadmap
- Trend chart (7‑day moving average)
- Component/Epic breakdowns
- YAML config & richer filters
- Testomat correlation (test runs ↔ QA cycle)
- Dockerfile & Cloud Run job
- Slack slash commands `/qa-snapshot`
