# Who still has access to the private repositories?

At 10:00 UTC a contractor leaves and a Payments engineer transfers to Support. At 10:15 the help desk wants to close both tickets. Your job is to compare each person's **approved role** with their **effective role** on three private GitHub repositories, then tell the correct owner what to do. Allow ten minutes. The example uses fictional tickets and runs offline.

## Read the tickets

| Ticket | Person | Approved outcome |
| --- | --- | --- |
| IAM-104 | Sam, contractor and outside collaborator, GitHub ID 831 | Remove all human access to `billing` and `release-tools`. |
| IAM-105 | Jo, organization member moving to Support, GitHub ID 912 | Reduce `payments-api` to Read. Jo still needs to consult the code while handling support tickets. |

**Effective role** means the access GitHub gives the person after combining the applicable grants. The collaborators endpoint reports the highest resulting role. Use separate evidence to explain its source. An outside collaborator can have direct repository access without organization membership, and only organization members can belong to teams. [Collaborators API](https://docs.github.com/en/rest/collaborators/collaborators#list-repository-collaborators) · [Outside collaborators](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-outside-collaborators/adding-outside-collaborators-to-repositories-in-your-organization)

## Make the call at 10:15

| Repository | Effective-access evidence | Separate evidence about the grant |
| --- | --- | --- |
| `billing` | At 10:09, Sam has Write. | The repository access review shows a direct Write grant to ID 831. Sam has never been an organization member. |
| `payments-api` | At 10:10, Jo has Write. | The direct Write grant ended at 10:02. The team roster still lists Jo in Payments, which has Write, and Support, which has Read. |
| `release-tools` | The last complete review showed Sam had Read at 09:50. A 10:08 export stopped after page one without finding Sam. | The release team has yet to supply the rest of the export. |

For each repository, write one sentence naming the decision, the evidence that supports it, and who owes the next action. Decide whether to remove Jo from Payments, Support, or both. Run the review from the repository root and compare the two snapshots.

```sh
python studies/iam-offboarding/review.py
```

<details>
<summary>Open the analyst's handoff</summary>

- **Billing maintainers** should remove Sam's direct grant and independently verify effective access. At 10:38 the complete review shows no role for ID 831.
- **Payments team owner** should remove Jo's obsolete Payments membership and keep the approved Support membership. At 10:45 the repository shows Read. This closes the transfer item without breaking Jo's new job.
- **Release engineering** should supply a complete post-departure review. The 09:50 result predates the departure, and a missing name on page one proves nothing about later pages. At 10:53 complete evidence verifies no access.

At 10:15 there are **two excess grants and one unverified item**. At 11:00 all three observations match approval. These are verification times. The ticket does not establish the precise time each permission changed.

</details>

## Inspect or change the evidence

The Python runner uses SQLite to join the ticket's stable user ID and repository to the most recent eligible observation. The fixture records completeness explicitly. `none` summarizes verified absence from a fully collected effective-access review of a known private repo. `NULL` means no reliable role was established. A failed request, missing page, or missing account mapping needs investigation. Only the three roles in these tickets are scored. Other role names require manual review. [Fixture data](fixtures.sql) · [Decision query](review.sql)

Try changing Jo's 10:45 role from `read` to `none`. The 11:00 result becomes **missing approved access**. A tool that called every removal a success would leave Support unable to do its work.

## A real GitHub case and the next project

GitHub's April 2022 investigation found that stolen OAuth user tokens issued to Heroku and Travis CI were used to download private repositories from dozens of organizations. Those were delegated application authorizations. The tickets above exercise human repository roles. [GitHub incident report](https://github.blog/news-insights/company-news/security-alert-stolen-oauth-user-tokens/)

**Continue with third-party OAuth access.** Compare an active build service, a retired reporting tool, and an integration whose owner is unknown. Use the business register, organization policy snapshots, and build checks to make a decision for each. [Work the OAuth review](../github-oauth-access/README.md)

**Then review deploy keys.** Map repository key fingerprints to the automation that uses them. A deploy key can continue to work after its creator loses access. An ownerless key should prompt a custody and dependency review. Record who uses it, its permission level and evidence of retirement or an approved owner. [GitHub deploy key guidance](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managing-deploy-keys)
