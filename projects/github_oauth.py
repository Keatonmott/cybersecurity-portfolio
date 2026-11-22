"""Review organization approvals for ordinary third-party GitHub OAuth apps."""

import argparse
from datetime import datetime
import json
from pathlib import Path


FIXTURE = Path(__file__).resolve().parents[1] / "studies" / "github-oauth-access" / "fixtures.json"


def instant(value):
    timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if timestamp.tzinfo is None:
        raise ValueError("Evidence timestamps must include a time zone.")
    return timestamp


def by_app(rows):
    index = {}
    for row in rows:
        key = row["app_id"]
        if key in index:
            raise ValueError(f"Conflicting evidence: duplicate application ID {key!r}")
        index[key] = row
    return index


def decide(app, approved, health, window, complete, restricted):
    if not restricted:
        return "verify policy", "Confirm that organization restrictions are enabled before using this approval list."
    if not complete or type(approved) is not bool:
        return "verify evidence", "Obtain a complete policy review with an explicit observation for this app."
    if app.get("lifecycle") == "retired":
        if approved:
            return "remove approval", "Have an organization owner deny this retired app and verify the new policy state."
        return "retirement verified", "File the dated organization denial as closure evidence."
    if app.get("lifecycle") != "active" or not app.get("owner") or not app.get("purpose"):
        return "investigate owner", "Identify the business owner and dependency, then record a retain or retire decision."
    if not approved:
        return "review service gap", "Ask the service owner whether the recorded need or the organization policy changed."
    if health and health.get("passed") is True:
        if window[0] <= instant(health["checked_at"]) <= window[1]:
            return "retain", "Keep the approval and file the successful build check with the owner's register entry."
    return "verify service", "Ask the service owner for a successful build check from this review window."


def review(data):
    register = by_app(data["applications"])
    reports = []
    for snapshot in data["snapshots"]:
        approvals = by_app(snapshot["approvals"])
        checks = by_app(snapshot["health_checks"])
        window = (instant(snapshot["window_start"]), instant(snapshot["as_of"]))
        if window[0] > window[1]:
            raise ValueError("Review window starts after the snapshot.")
        rows = []
        for app_id in dict.fromkeys((*register, *approvals)):
            app = register.get(app_id, {})
            approved = approvals.get(app_id, {}).get("approved")
            check = checks.get(app_id)
            decision, action = decide(app, approved, check, window,
                                      snapshot["complete"] is True, snapshot["restrictions_enabled"] is True)
            rows.append({
                "app_id": app_id, "application": app.get("name", app_id), "ticket": app.get("ticket"),
                "owner": app.get("owner"), "review_team": app.get("review_team", "Organization Security"),
                "purpose": app.get("purpose"), "lifecycle": app.get("lifecycle", "unknown"),
                "approved": approved, "health_check": check, "decision": decision, "next_action": action,
            })
        reports.append({
            "as_of": snapshot["as_of"], "window_start": snapshot["window_start"], "evidence_ref": snapshot["evidence_ref"],
            "complete": snapshot["complete"], "restrictions_enabled": snapshot["restrictions_enabled"], "applications": rows,
        })
    return {"organization": data["organization"], "reviews": reports}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=FIXTURE, help="normalized local review fixture")
    parser.add_argument("--json", action="store_true", help="emit the evidence report as JSON")
    args = parser.parse_args()
    try:
        report = review(json.loads(args.input.read_text(encoding="utf-8")))
    except (OSError, KeyError, ValueError, TypeError) as error:
        parser.error(str(error))
    if args.json:
        print(json.dumps(report, indent=2))
        return
    for snapshot in report["reviews"]:
        print(f"\n{snapshot['as_of']}  {snapshot['evidence_ref']}")
        for row in snapshot["applications"]:
            print(f"{row['ticket'] or 'unassigned':10} {row['application']:16} "
                  f"{row['decision']:21} {row['review_team']}")


if __name__ == "__main__":
    main()
