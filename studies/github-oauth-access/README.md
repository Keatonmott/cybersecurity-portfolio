# Which OAuth applications should keep GitHub organization approval?

You own the quarterly access review for the fictional `example-workshop` organization. Three ordinary third-party OAuth apps have approval at 09:00 UTC. Release Engineering is shipping a package this morning. Before recommending a change, identify what still depends on each app, who owns the decision, and what evidence would let you close its ticket.

## Why review delegated access?

In April 2022, GitHub reported that stolen OAuth user tokens issued to Heroku and Travis CI had been used to download private repositories from dozens of organizations. GitHub recommended reviewing which applications users and organizations had authorized. This exercise applies that recommendation to fictional business records. [GitHub incident report](https://github.blog/news-insights/company-news/security-alert-stolen-oauth-user-tokens/)

For this exercise, an **organization approval** allows an ordinary third-party OAuth app to access private organization resources on behalf of an authorizing user, subject to that user's permissions and the token's scopes. The organization has OAuth app restrictions enabled. A personal token revocation and a GitHub App installation are separate records with different owners. The exercise checks only the organization's policy for these three OAuth apps. [GitHub organization policy](https://docs.github.com/en/organizations/managing-oauth-access-to-your-organizations-data/about-oauth-app-access-restrictions) · [GitHub credential types](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/github-credential-types)

## Work the 09:00 review

| Ticket | What you know | Decision to make |
| --- | --- | --- |
| OAUTH-201 · Build Courier | Release Engineering uses it to deliver results for a private packaging repository. The build check passed at 08:56. | What evidence justifies keeping approval through the release? |
| OAUTH-202 · Weekly Digest | Developer Experience retired the weekly activity report. The organization policy snapshot still lists the integration as approved. | Who can remove approval, and what observation would close the ticket? |
| OAUTH-203 · Archive Bridge | The organization has approved it. The register lists neither a service owner nor a business purpose. | Who investigates, and what would justify keeping or retiring it? |

Write a one-sentence ticket update for each application before looking at the second review. Then run the decisions from the repository root. Python's standard library is the only dependency.

```sh
python -m projects.github_oauth
```

<details>
<summary>Compare your decisions with the 11:00 handoff</summary>

| Application | 09:00 decision | 11:00 evidence and handoff |
| --- | --- | --- |
| Build Courier | **Retain.** Release Engineering owns a current dependency and has a successful check. | The app remains approved and the 10:55 check passed. Keep the build running. |
| Weekly Digest | **Remove approval.** Developer Experience should coordinate with a GitHub organization owner. | The complete 11:00 policy observation explicitly records approval denied. File `ORG-REVIEW-1100` and close the organization approval ticket. Personal authorizations would require separate evidence. [GitHub's organization denial procedure](https://docs.github.com/en/organizations/managing-oauth-access-to-your-organizations-data/denying-access-to-a-previously-approved-oauth-app-for-your-organization) |
| Archive Bridge | **Investigate owner.** Organization Security owns the follow-up. | Approval remains and ownership is unresolved. Ask the teams listed in the service catalog for dependency evidence. If an owner can document a current use, record both and reassess. Otherwise send a retirement proposal to the organization owner and verify the resulting policy state. |

The second review verifies one retirement and one working build. The ownership investigation stays open.

</details>

## Check the evidence

The register gives each app a stable ID. Each snapshot has a review window, a policy evidence reference, and explicit approval observations. These are normalized training records. The program reads local files and prints decisions. A successful build describes that service's health during the window. It cannot establish which repositories an app accessed or whether its authorizations were ever abused.

- Read the two snapshots in the [synthetic fixture](fixtures.json) and compare them with the [generated report](../../evidence/github-oauth-review.json). Use `python -m projects.github_oauth --json` to reproduce the report.
- In a copy of the fixture, set the second snapshot's `complete` to `false`. Run `python -m projects.github_oauth --input path/to/copy.json`. Each ticket asks for better evidence, including the one previously marked retired.
- Restore completeness, then change the 10:55 build check to 08:56. The older success no longer qualifies in the second review window. Release Engineering gets a request for fresh evidence.

The rule covers ordinary third-party OAuth apps. Privileged OAuth apps have distinct policy behavior. Separate inventories would be needed for GitHub App installations, deploy keys, and individual user authorizations. [Decision logic](../../projects/github_oauth.py) · [Regression tests](../../tests/test_github_oauth.py)
