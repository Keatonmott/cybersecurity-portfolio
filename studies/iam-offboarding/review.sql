-- Compare the approved and observed roles at one review time.
WITH latest AS (
    SELECT s.*, e.seen_at, e.role, e.complete,
           ROW_NUMBER() OVER (
               PARTITION BY s.ticket, s.user_id, s.repo
               ORDER BY e.seen_at DESC
           ) AS recency
    FROM scope AS s
    LEFT JOIN evidence AS e
        ON e.user_id = s.user_id AND e.repo = s.repo AND e.seen_at <= :as_of
    WHERE s.effective_from <= :as_of
)
SELECT ticket, repo, expected, role, seen_at,
       CASE
           WHEN seen_at IS NULL OR seen_at < effective_from OR complete = 0 THEN 'unverified'
           WHEN role IS NULL OR role NOT IN ('none', 'read', 'write') THEN 'unverified'
           WHEN role = expected THEN 'matches approval'
           WHEN expected = 'none' OR role = 'write' THEN 'excess access'
           WHEN role = 'none' AND expected = 'read' THEN 'missing approved access'
           ELSE 'unverified'
       END AS decision, owner
FROM latest
WHERE recency = 1
ORDER BY ticket, repo;
