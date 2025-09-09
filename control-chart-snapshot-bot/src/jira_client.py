
import requests

class JiraClient:
    def __init__(self, base_url, email, token):
        self.base = base_url.rstrip('/')
        self.auth = (email, token)
        self.headers = {"Accept": "application/json"}

    def search_issues(self, jql, max_results=100):
        start = 0
        out = []
        while True:
            r = requests.post(
                f"{self.base}/rest/api/3/search",
                auth=self.auth,
                headers=self.headers,
                json={
                    "jql": jql,
                    "startAt": start,
                    "maxResults": max_results,
                    "expand": ["changelog"]
                }
            )
            r.raise_for_status()
            data = r.json()
            out.extend(data.get("issues", []))
            total = data.get("total", 0)
            if start + max_results >= total:
                break
            start += max_results
        return out
