import json
import unittest

from projects.github_oauth import FIXTURE, review


class OAuthReviewTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.later = self.data["snapshots"][-1]

    def decisions(self, index=-1):
        rows = review(self.data)["reviews"][index]["applications"]
        return {row["app_id"]: row["decision"] for row in rows}

    def test_retirement_closes_only_on_second_snapshot(self):
        self.assertEqual(self.decisions(0), {
            "build-01": "retain", "reports-02": "remove approval", "sync-03": "investigate owner",
        })
        self.assertEqual(self.decisions(), {
            "build-01": "retain", "reports-02": "retirement verified", "sync-03": "investigate owner",
        })

    def test_missing_partial_or_disabled_policy_cannot_verify_retirement(self):
        self.later["complete"] = False
        self.assertEqual(self.decisions()["reports-02"], "verify evidence")
        self.later["complete"] = True
        self.later["restrictions_enabled"] = False
        self.assertEqual(self.decisions()["reports-02"], "verify policy")
        self.later["restrictions_enabled"] = True
        self.later["approvals"] = [row for row in self.later["approvals"] if row["app_id"] != "reports-02"]
        self.assertEqual(self.decisions()["reports-02"], "verify evidence")

    def test_stale_future_or_failed_health_checks_cannot_validate_the_build(self):
        check = self.later["health_checks"][0]
        for timestamp, passed in (("08:56:00", True), ("11:01:00", True), ("10:55:00", False)):
            with self.subTest(timestamp=timestamp, passed=passed):
                check.update(checked_at=f"2026-01-12T{timestamp}Z", passed=passed)
                self.assertEqual(self.decisions()["build-01"], "verify service")

    def test_unregistered_approval_enters_the_investigation_queue(self):
        self.later["approvals"].append({"app_id": "unlisted-04", "approved": True})
        self.assertEqual(self.decisions()["unlisted-04"], "investigate owner")

    def test_conflicting_rows_cannot_close_a_ticket(self):
        self.later["approvals"].append({"app_id": "reports-02", "approved": True})
        with self.assertRaisesRegex(ValueError, "duplicate application ID"):
            review(self.data)
