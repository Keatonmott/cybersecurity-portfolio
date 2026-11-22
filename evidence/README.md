# Sample results

Rebuild these files from the repository root with `python -m tools.build_evidence`. All inputs are synthetic.

| File | What to inspect |
| --- | --- |
| [Risky inventory](cloud-risky.json) and [corrected inventory](cloud-safe.json) | Match each finding to a resource and compare the two runs. |
| [Identity alert](identity-alerts.json) | The two records share a target user and are two minutes apart. |
| [GitHub OAuth approvals](github-oauth-review.json) | Follow three applications across two dated reviews. Each row records an organization policy observation, decision, accountable queue, and next action. |
| [API authorization](api-authorization.json) | Compare the owner's result with the result for another user and for a missing document. |
| [Assistant evaluation](ai-evaluation.json) | Compare each simulator response with its expected answer and disclosure check. |
