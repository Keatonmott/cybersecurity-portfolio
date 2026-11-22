"""Detect rapid access-key creation followed by admin policy attachment."""

import argparse
from datetime import datetime, timedelta, timezone
import json
from operator import itemgetter
from pathlib import Path


WINDOW = timedelta(minutes=10)


def parse_time(value):
    timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if timestamp.tzinfo is None:
        raise ValueError("timestamps must have a timezone")
    return timestamp.astimezone(timezone.utc)


def detect(events):
    """Return one alert per qualifying policy attachment."""
    candidates = []
    for event in events:
        when = parse_time(event["timestamp"])
        if event.get("outcome") != "success" or not event.get("target_user"):
            continue
        if event.get("event") == "CreateAccessKey" or (
            event.get("event") == "AttachUserPolicy" and event.get("policy") == "AdministratorAccess"
        ):
            candidates.append((when, event))

    candidates.sort(key=itemgetter(0))
    recent_keys = {}
    alerts = []
    for when, event in candidates:
        user = event["target_user"]
        if event["event"] == "CreateAccessKey":
            recent_keys[user] = (when, event)
            continue
        key = recent_keys.get(user)
        if key and when - key[0] <= WINDOW:
            alerts.append({
                "rule_id": "IDENTITY-001",
                "severity": "high",
                "target_user": user,
                "key_event": key[1],
                "policy_event": event,
                "reason": "Access key created, then admin policy attached within ten minutes.",
            })
    return alerts


def iter_events(path):
    with path.open(encoding="utf-8") as lines:
        for line in lines:
            if line.strip():
                yield json.loads(line)


def load_events(path):
    return list(iter_events(path))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("events", type=Path)
    args = parser.parse_args()
    alerts = detect(iter_events(args.events))
    print(json.dumps({"event_file": str(args.events), "alert_count": len(alerts),
                      "alerts": alerts}, indent=2))


if __name__ == "__main__":
    main()
