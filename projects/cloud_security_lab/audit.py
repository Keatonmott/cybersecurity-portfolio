"""Check storage access, IAM permissions and audit logging in a JSON snapshot."""

import argparse
import json
from pathlib import Path


def audit(snapshot):
    """Return findings without mutating the supplied snapshot."""
    resources = snapshot.get("resources") if isinstance(snapshot, dict) else None
    if not isinstance(resources, list):
        raise ValueError("snapshot must contain a resources list")

    findings = []
    for resource in resources:
        if not isinstance(resource, dict) or any(
            not isinstance(resource.get(field), str) or not resource[field].strip()
            for field in ("id", "type")
        ):
            raise ValueError("each resource needs an id and type")
        kind = resource["type"]
        resource_id = resource["id"]
        if kind not in {"iam_policy", "object_storage", "audit_logging"}:
            raise ValueError(f"{resource_id}: unsupported resource type {kind!r}")
        if kind == "object_storage" and not isinstance(resource.get("public_read"), bool):
            raise ValueError(f"{resource_id}: public_read must be a boolean")
        if kind == "iam_policy":
            for field in ("actions", "resources"):
                values = resource.get(field)
                if not isinstance(values, list) or not values or not all(
                    isinstance(value, str) and value.strip() for value in values
                ):
                    raise ValueError(f"{resource_id}: {field} must be a nonempty list of names")
        if kind == "object_storage" and resource.get("public_read") is True:
            findings.append({"id": "CLOUD-001", "severity": "high", "resource": resource_id,
                             "problem": "Object storage permits public reads.",
                             "remediation": "Block public access and review bucket and object policies."})
        elif kind == "iam_policy" and ("*" in resource.get("actions", []) or "*" in resource.get("resources", [])):
            findings.append({"id": "CLOUD-002", "severity": "high", "resource": resource_id,
                             "problem": "IAM policy contains a wildcard action or resource.",
                             "remediation": "Grant only required actions on named resources."})
        elif kind == "audit_logging" and resource.get("enabled") is not True:
            findings.append({"id": "CLOUD-003", "severity": "high", "resource": resource_id,
                             "problem": "Audit logging is disabled or unconfirmed.",
                             "remediation": "Enable audit logging and protect its destination."})
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    args = parser.parse_args()
    try:
        snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
        findings = audit(snapshot)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps({"snapshot": str(args.snapshot), "finding_count": len(findings),
                      "findings": findings}, indent=2))


if __name__ == "__main__":
    main()
