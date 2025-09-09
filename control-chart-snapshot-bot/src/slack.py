
import requests
import json

def post_message(token, channel_id, text):
    r = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        data=json.dumps({"channel": channel_id, "text": text}),
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    if not data.get("ok"):
        raise RuntimeError(f"Slack error: {data}")
    return data

def upload_file(token, channel_id, path, title):
    with open(path, "rb") as f:
        r = requests.post(
            "https://slack.com/api/files.upload",
            headers={"Authorization": f"Bearer {token}"},
            data={"channels": channel_id, "title": title},
            files={"file": f},
            timeout=60,
        )
    r.raise_for_status()
    data = r.json()
    if not data.get("ok"):
        raise RuntimeError(f"Slack error: {data}")
    return data
