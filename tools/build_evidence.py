"""Build the portfolio's JSON reports from the local fixtures."""

import json
from pathlib import Path

from projects.ai_security.evaluate import CASES_PATH, evaluate
from projects.cloud_security_lab.audit import audit
from projects.cloud_security_lab.detect import detect, iter_events
from projects.github_oauth import FIXTURE as OAUTH_FIXTURE, review as review_oauth
from projects.secure_api.demo import access_matrix


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "evidence"
CLOUD = ROOT / "projects" / "cloud_security_lab" / "fixtures"


def write_json(name, value):
    with (OUTPUT / name).open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def main():
    OUTPUT.mkdir(exist_ok=True)
    for name in ("risky", "safe"):
        snapshot = json.loads((CLOUD / f"{name}.json").read_text(encoding="utf-8"))
        findings = audit(snapshot)
        write_json(f"cloud-{name}.json", {"finding_count": len(findings), "findings": findings})

    alerts = detect(iter_events(CLOUD / "events.jsonl"))
    write_json("identity-alerts.json", {"alert_count": len(alerts), "alerts": alerts})
    write_json("api-authorization.json", {"checks": access_matrix()})

    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    evaluations = [evaluate(cases, mode) for mode in ("baseline", "guarded")]
    write_json("ai-evaluation.json", {"evaluations": evaluations})
    write_json("github-oauth-review.json", review_oauth(json.loads(OAUTH_FIXTURE.read_text(encoding="utf-8"))))
    print("Wrote six JSON reports to evidence/.")


if __name__ == "__main__":
    main()
