# Service account access review

At 10:00 UTC on January 10, the actor `automation` created an access key for `service-reports`. Two minutes later, the same actor attached `AdministratorAccess` to the account. Both events succeeded and share the source address `192.0.2.10`. The fixture ends before it records any use of the key. [Alert evidence](../../evidence/identity-alerts.json)

Compare the change with the approved provisioning request. If the grant was unauthorized, preserve the events, disable the key, remove the grant and check the account's activity during those two minutes and afterward.

## Two sequences that produced no alert

At 11:00 a key was created for `service-backup`, but the subsequent policy attachment named a different user. At 12:00 the target user matched, but 20 minutes elapsed before the grant. An approved rotation followed by a legitimate administrative grant could satisfy both conditions, so the analyst still needs the change record.

## Inventory findings

| Resource | Original setting | Corrected setting |
| --- | --- | --- |
| `reports-bucket` | Public reads enabled | Public reads disabled |
| `report-reader` | All actions on all resources | `s3:GetObject` for objects in the reports bucket |
| `organization-audit` | Logging disabled | Logging enabled |

The inventory and event stream are separate synthetic fixtures. The three posture findings establish configuration risk. The event pair by itself cannot establish whether anyone read a report. [Original findings](../../evidence/cloud-risky.json) · [Results after remediation](../../evidence/cloud-safe.json)
