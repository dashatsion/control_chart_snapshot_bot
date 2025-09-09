
from datetime import datetime
import pandas as pd

def _to_dt(iso):
    # Jira dates like '2025-07-08T12:34:56.789+0000' or ISO with Z
    iso = iso.replace('Z', '+00:00')
    if '+' in iso[19:] and iso.count(':') == 2:
        # normalize '+0000' to '+00:00'
        if iso[-5] in ['+', '-'] and iso[-3] != ':':
            iso = iso[:-2] + ':' + iso[-2:]
    return datetime.fromisoformat(iso)

def parse_first_completed_qa_cycle(issue, qa_status, done_status):
    qa_in, done_at = None, None
    histories = issue.get("changelog", {}).get("histories", [])
    for hist in sorted(histories, key=lambda h: h.get("created")):
        created = hist.get("created")
        if not created:
            continue
        at = _to_dt(created)
        for item in hist.get("items", []):
            if item.get("field") == "status":
                to_ = item.get("toString")
                if to_ == qa_status and qa_in is None:
                    qa_in = at
                elif qa_in is not None and to_ == done_status and done_at is None:
                    done_at = at
                    break
        if qa_in and done_at:
            break
    if qa_in and done_at and done_at > qa_in:
        days = (done_at - qa_in).total_seconds() / 86400.0
        return days
    return None

def build_dataframe(issues, qa_status, done_status):
    rows = []
    for it in issues:
        key = it.get("key")
        cycle = parse_first_completed_qa_cycle(it, qa_status, done_status)
        if cycle is not None:
            rows.append({"issue": key, "qa_cycle_days": cycle})
    return pd.DataFrame(rows)

def summarize(df):
    if df.empty:
        return {"count": 0, "mean": 0, "median": 0, "p75": 0}
    s = df["qa_cycle_days"]
    return {
        "count": int(s.count()),
        "mean": round(float(s.mean()), 2),
        "median": round(float(s.median()), 2),
        "p75": round(float(s.quantile(0.75)), 2),
    }
