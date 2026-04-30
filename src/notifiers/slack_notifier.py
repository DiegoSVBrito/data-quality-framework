import json
import os
import requests


def send_slack_alert(suite_name: str, results: dict, webhook_url: str = None):
    webhook = webhook_url or os.getenv("SLACK_WEBHOOK_URL")
    if not webhook:
        print("SLACK_WEBHOOK_URL not configured, skipping Slack notification")
        return

    failed = [r for r in results["results"] if not r["success"]]
    failed_text = "\n".join(f"- {r['expectation']}: {r['kwargs']}" for r in failed)

    payload = {
        "text": f"Data Quality Alert: {suite_name}",
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"Quality Alert: {suite_name}"},
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Total:* {results['total']}"},
                    {"type": "mrkdwn", "text": f"*Passed:* {results['passed']}"},
                    {"type": "mrkdwn", "text": f"*Failed:* {results['failed']}"},
                    {"type": "mrkdwn", "text": f"*Rate:* {results['success_rate']:.1f}%"},
                ],
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": f"*Failed expectations:*\n{failed_text}"}},
        ],
    }

    response = requests.post(webhook, json=payload, timeout=10)
    response.raise_for_status()
