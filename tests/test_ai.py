import json
import unittest

from projects.ai_security.evaluate import CASES_PATH, CANARY, evaluate, respond


class AiEvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))

    def test_baseline_exposes_canary_on_attack_cases(self):
        result = evaluate(self.cases, "baseline")
        self.assertEqual((result["attack_successes"], result["attack_cases"]), (3, 3))

    def test_guarded_mode_preserves_tasks_without_canary(self):
        result = evaluate(self.cases, "guarded")
        self.assertEqual(result["attack_successes"], 0)
        self.assertEqual((result["benign_completed"], result["benign_cases"]), (2, 2))
        self.assertTrue(all(CANARY not in item["answer"] for item in result["results"]))

    def test_unknown_mode_is_rejected(self):
        with self.assertRaises(ValueError):
            respond("question", "document", "unknown")

    def test_mislabeled_case_cannot_drop_out_of_the_totals(self):
        case = dict(self.cases[0], kind="unlabeled")
        with self.assertRaisesRegex(ValueError, case["id"]):
            evaluate([case], "guarded")


if __name__ == "__main__":
    unittest.main()
