import sqlite3
import unittest
from pathlib import Path


STUDY = Path(__file__).resolve().parents[1] / "studies" / "iam-offboarding"


class GitHubAccessReviewTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.addCleanup(self.db.close)
        self.db.executescript((STUDY / "fixtures.sql").read_text(encoding="utf-8"))
        self.query = (STUDY / "review.sql").read_text(encoding="utf-8")

    def decisions(self, as_of):
        rows = self.db.execute(self.query, {"as_of": as_of})
        return {repo: decision for _, repo, _, _, _, decision, _ in rows}

    def test_later_confirmations_cannot_close_an_earlier_review(self):
        self.assertEqual(self.decisions("10:15"), {
            "billing": "excess access",
            "payments-api": "excess access",
            "release-tools": "unverified",
        })
        self.assertEqual(list(self.decisions("11:00").values()), ["matches approval"] * 3)

    def test_wrong_identity_or_stale_export_cannot_prove_removal(self):
        self.db.execute("UPDATE evidence SET user_id = 999 WHERE repo = 'billing'")
        self.db.execute("DELETE FROM evidence WHERE repo = 'release-tools' AND seen_at >= '10:00'")
        decisions = self.decisions("11:00")
        self.assertEqual(decisions["billing"], "unverified")
        self.assertEqual(decisions["release-tools"], "unverified")

    def test_transfer_requires_preserving_approved_read_access(self):
        self.db.execute("UPDATE evidence SET role = 'none' WHERE repo = 'payments-api' AND seen_at = '10:45'")
        self.assertEqual(self.decisions("11:00")["payments-api"], "missing approved access")
