import json
from pathlib import Path
import unittest

from projects.cloud_security_lab.audit import audit
from projects.cloud_security_lab.detect import detect, load_events


FIXTURES = Path(__file__).resolve().parents[1] / "projects" / "cloud_security_lab" / "fixtures"


class CloudLabTests(unittest.TestCase):
    def test_risky_snapshot_has_three_distinct_findings(self):
        snapshot = json.loads((FIXTURES / "risky.json").read_text(encoding="utf-8"))
        self.assertEqual({item["id"] for item in audit(snapshot)},
                         {"CLOUD-001", "CLOUD-002", "CLOUD-003"})

    def test_safe_snapshot_has_no_findings(self):
        snapshot = json.loads((FIXTURES / "safe.json").read_text(encoding="utf-8"))
        self.assertEqual(audit(snapshot), [])

    def test_missing_resource_list_fails_closed(self):
        with self.assertRaises(ValueError):
            audit({})

    def test_incomplete_storage_and_policy_cannot_pass_as_clean(self):
        for resource in [
            {"id": "bucket", "type": "object_storage", "public_read": "false"},
            {"id": "reader", "type": "iam_policy", "actions": ["s3:GetObject"]},
            {"id": "reader", "type": "iam_policy", "actions": "s3:GetObject", "resources": ["reports"]},
            {"id": "bucket", "type": "object_storge"},
        ]:
            with self.subTest(resource=resource), self.assertRaises(ValueError):
                audit({"resources": [resource]})

    def test_fixture_detects_only_same_user_within_window(self):
        alerts = detect(load_events(FIXTURES / "events.jsonl"))
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["target_user"], "service-reports")

    def test_failed_policy_attachment_does_not_alert(self):
        events = load_events(FIXTURES / "events.jsonl")[:2]
        events[1]["outcome"] = "failure"
        self.assertEqual(detect(events), [])

    def test_out_of_order_events_at_ten_minute_boundary(self):
        key, policy = load_events(FIXTURES / "events.jsonl")[:2]
        policy["timestamp"] = "2026-01-10T05:10:00-05:00"
        self.assertEqual(len(detect([policy, key])), 1)
        policy["timestamp"] = "2026-01-10T05:10:01-05:00"
        self.assertEqual(detect([policy, key]), [])


if __name__ == "__main__":
    unittest.main()
