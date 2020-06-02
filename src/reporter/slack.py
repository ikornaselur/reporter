import os

import httpx

from . import models


def notify(report: models.Report) -> None:
    hook = os.environ.get("SLACK_HOOK")
    if not hook:
        return

    payload = {
        "text": "A new error has just been reported",
        "icon_emoji": ":warning:",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*JSON Input*\n```{report.json_input}```",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Python Output*\n```{report.python_output}```",
                },
            },
        ],
    }
    response = httpx.post(hook, json=payload)
    response.raise_for_status()
