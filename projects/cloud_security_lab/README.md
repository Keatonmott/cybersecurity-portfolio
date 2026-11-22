# Cloud posture and identity detection

The reports bucket should be private, its reader should have access only to report objects, and audit logging should be on. The fixtures show that inventory before and after remediation. A separate event log records an administrator granting full access to a service account two minutes after creating a key for it.

## Reproduce the findings

Run these commands from the repository root. Both tools read local synthetic data.

```powershell
python -m projects.cloud_security_lab.audit projects/cloud_security_lab/fixtures/risky.json
python -m projects.cloud_security_lab.audit projects/cloud_security_lab/fixtures/safe.json
python -m projects.cloud_security_lab.detect projects/cloud_security_lab/fixtures/events.jsonl
python -m unittest tests.test_cloud -v
```

| Input | Expected result |
| --- | --- |
| `risky.json` | Three findings, one each for public reads, wildcard IAM scope and disabled logging |
| `safe.json` | Zero findings under those three checks |
| `events.jsonl` | One alert for `service-reports`, including both source events |

## Rule scope

The audit checks the resources present in a snapshot. It rejects unsupported resource types and incomplete storage or IAM entries. The IAM check looks for a literal `*` as an entire action or resource. A resource ARN ending in `/*` still scopes the policy to the named bucket's objects. Effective AWS permissions also depend on conditions, resource policies and organization controls outside this fixture.

The detector matches two successful events for the same target user within ten minutes, inclusive. It reads the file line by line, normalizes each timestamp to UTC and keeps candidate events in memory for sorting. Events with identical timestamps retain file order. Each alert includes the most recent preceding key creation for that user.

The [investigation report](report.md) explains which record to check next. The [Terraform example](terraform/README.md) defines the storage controls.
