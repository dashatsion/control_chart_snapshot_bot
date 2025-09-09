
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Cfg:
    JIRA_BASE_URL: str
    JIRA_EMAIL: str
    JIRA_API_TOKEN: str
    JIRA_PROJECT_KEYS: str
    JIRA_QA_STATUS: str
    JIRA_DONE_STATUS: str
    LOOKBACK_DAYS: int
    WINDOW_DAYS: int
    SLACK_BOT_TOKEN: str
    SLACK_CHANNEL_ID: str
    TIMEZONE: str
    ANOMALY_THRESHOLD_DAYS: int

def get_cfg():
    return Cfg(
        JIRA_BASE_URL=os.getenv("JIRA_BASE_URL", ""),
        JIRA_EMAIL=os.getenv("JIRA_EMAIL", ""),
        JIRA_API_TOKEN=os.getenv("JIRA_API_TOKEN", ""),
        JIRA_PROJECT_KEYS=os.getenv("JIRA_PROJECT_KEYS", ""),
        JIRA_QA_STATUS=os.getenv("JIRA_QA_STATUS", "Ready for QA"),
        JIRA_DONE_STATUS=os.getenv("JIRA_DONE_STATUS", "Done"),
        LOOKBACK_DAYS=int(os.getenv("LOOKBACK_DAYS", "60")),
        WINDOW_DAYS=int(os.getenv("WINDOW_DAYS", "30")),
        SLACK_BOT_TOKEN=os.getenv("SLACK_BOT_TOKEN", ""),
        SLACK_CHANNEL_ID=os.getenv("SLACK_CHANNEL_ID", ""),
        TIMEZONE=os.getenv("TIMEZONE", "America/New_York"),
        ANOMALY_THRESHOLD_DAYS=int(os.getenv("ANOMALY_THRESHOLD_DAYS", "7")),
    )
