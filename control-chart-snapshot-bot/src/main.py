
import os
from config import get_cfg
from jira_client import JiraClient
from compute import build_dataframe, summarize
from chart import plot_distribution
from slack import post_message, upload_file

def main():
    cfg = get_cfg()

    if not (cfg.JIRA_BASE_URL and cfg.JIRA_EMAIL and cfg.JIRA_API_TOKEN):
        raise SystemExit("Jira credentials are missing. Set env vars or .env file.")
    if not (cfg.SLACK_BOT_TOKEN and cfg.SLACK_CHANNEL_ID):
        raise SystemExit("Slack credentials are missing. Set env vars or .env file.")
    if not cfg.JIRA_PROJECT_KEYS:
        raise SystemExit("Set JIRA_PROJECT_KEYS (comma-separated).")

    client = JiraClient(cfg.JIRA_BASE_URL, cfg.JIRA_EMAIL, cfg.JIRA_API_TOKEN)
    jql = (
        f'project in ({cfg.JIRA_PROJECT_KEYS}) '
        f'AND status WAS "{cfg.JIRA_QA_STATUS}" DURING (-{cfg.LOOKBACK_DAYS}d, now())'
    )
    issues = client.search_issues(jql)

    df = build_dataframe(issues, cfg.JIRA_QA_STATUS, cfg.JIRA_DONE_STATUS)
    stats = summarize(df)

    if stats["count"] == 0:
        post_message(cfg.SLACK_BOT_TOKEN, cfg.SLACK_CHANNEL_ID, ":zzz: No QA cycle data this period.")
        return

    out = "qa_cycle_histogram.png"
    plot_distribution(df, out)

    text = (
        "*QA Control Chart Snapshot*\n"
        f"Issues: {stats['count']}\n"
        f"Mean: {stats['mean']}d | Median: {stats['median']}d | P75: {stats['p75']}d"
    )
    post_message(cfg.SLACK_BOT_TOKEN, cfg.SLACK_CHANNEL_ID, text)
    upload_file(cfg.SLACK_BOT_TOKEN, cfg.SLACK_CHANNEL_ID, out, "QA Cycle Time — Distribution")

if __name__ == "__main__":
    main()
