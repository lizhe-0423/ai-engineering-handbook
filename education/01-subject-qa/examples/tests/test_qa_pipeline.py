"""Business boundaries for the small subject Q&A example."""
import copy
import json
import sys
import unittest
from pathlib import Path

EXAMPLES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXAMPLES))
from qa_core import compose_messages, plan_answer, validate_response


def fixture():
    return {
        "courses": {
            "math": {"subject": "数学", "teacher_style": "先提示变形步骤", "allow_direct": True},
            "physics": {"subject": "物理", "teacher_style": "先检查量和单位", "allow_direct": False},
        },
        "questions": [{"id": "ineq-01", "course_id": "math", "status": "approved",
                       "text": "解不等式 2x+3>7", "hint": "先在两边同时减去 3。",
                       "answer": "2x>4，两边除以正数 2，得 x>2。"}],
        "materials": [{"id": "units", "course_id": "physics", "status": "approved",
                       "title": "速度单位", "text": "速度单位换算：1 km/h = 1/3.6 m/s。"}],
    }


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.data = fixture()

    def rag(self):
        return plan_answer("速度 72 km/h 怎么换算？", "physics", self.data)

    def response(self, **changes):
        value = {"reply": "先统一单位。", "next_action": "explain",
                 "citations": [{"material_id": "units", "quote": "1 km/h = 1/3.6 m/s"}]}
        value.update(changes)
        return json.dumps(value, ensure_ascii=False)

    def test_approved_unique_bank_returns_selected_hint_or_solution(self):
        hint = plan_answer("解不等式 2x+3>7", "math", self.data)
        answer = plan_answer("解不等式 2x+3>7", "math", self.data, level="solution")
        self.assertEqual(hint["route"], "curated")
        self.assertEqual(hint["state"], "answered")
        self.assertEqual(hint["reply"], self.data["questions"][0]["hint"])
        self.assertEqual(answer["reply"], self.data["questions"][0]["answer"])
        self.assertFalse(hint["model_call_performed"])

    def test_different_operator_or_number_is_not_same_question(self):
        for question in ["解不等式 2x+3<7", "解不等式 2x+3>8"]:
            with self.subTest(question=question):
                self.assertNotEqual(plan_answer(question, "math", self.data)["route"], "curated")

    def test_whitespace_normalization_keeps_word_boundaries(self):
        self.assertEqual(plan_answer("解不等式  2x+3>7", "math", self.data)["route"], "curated")
        self.data["questions"][0]["text"] = "ab cd"
        self.assertNotEqual(plan_answer("a bcd", "math", self.data)["route"], "curated")

    def test_duplicate_approved_question_requires_teacher(self):
        duplicate = copy.deepcopy(self.data["questions"][0])
        duplicate["id"] = "conflict"
        duplicate["answer"] = "错误答案"
        self.data["questions"].append(duplicate)
        self.assertEqual(plan_answer("解不等式 2x+3>7", "math", self.data)["route"], "teacher_review")

    def test_unapproved_and_other_course_bank_entries_are_excluded(self):
        self.data["questions"][0]["status"] = "draft"
        self.assertEqual(plan_answer("解不等式 2x+3>7", "math", self.data)["route"], "direct")
        self.data["questions"][0]["status"] = "approved"
        self.data["questions"][0]["course_id"] = "physics"
        self.assertEqual(plan_answer("解不等式 2x+3>7", "math", self.data)["route"], "direct")

    def test_rag_is_a_prepared_request_not_generated_answer(self):
        plan = self.rag()
        self.assertEqual(plan["route"], "rag")
        self.assertEqual(plan["state"], "model_required")
        self.assertIsNone(plan["reply"])
        self.assertFalse(plan["model_call_performed"])
        self.assertEqual([m["id"] for m in plan["evidence"]], ["units"])

    def test_material_filter_applies_before_ranking(self):
        for course, status in [("math", "approved"), ("physics", "draft")]:
            other = dict(self.data["materials"][0], id=course + status, course_id=course, status=status)
            self.data["materials"].append(other)
        self.assertEqual([m["id"] for m in self.rag()["evidence"]], ["units"])

    def test_direct_generation_needs_course_permission(self):
        self.assertEqual(plan_answer("半径3cm的圆面积", "math", self.data)["route"], "direct")
        self.assertEqual(plan_answer("牛顿第三定律", "physics", self.data)["route"], "teacher_review")

    def test_uncertain_input_requests_confirmation(self):
        plan = plan_answer("2x+3?7", "math", self.data, input_confirmed=False)
        self.assertEqual(plan["route"], "ask_clarification")
        self.assertFalse(plan["model_call_performed"])

    def test_unknown_course_empty_question_and_invalid_level_rejected(self):
        for args, kwargs in [(("题", "unknown", self.data), {}),
                             ((" ", "math", self.data), {}),
                             (("题", "math", self.data), {"level": "admin"})]:
            with self.subTest(args=args[:2], kwargs=kwargs):
                with self.assertRaises(ValueError):
                    plan_answer(*args, **kwargs)

    def test_course_policy_and_untrusted_question_have_separate_roles(self):
        plan = self.rag()
        messages = compose_messages(plan)
        self.assertEqual([m["role"] for m in messages], ["system", "user"])
        self.assertIn("先检查量和单位", messages[0]["content"])
        self.assertIn("hint", messages[0]["content"])
        self.assertIn("units", messages[1]["content"])
        self.assertIn("速度 72 km/h", messages[1]["content"])

    def test_valid_cited_result_still_needs_content_review(self):
        result = validate_response(self.rag(), self.response())
        self.assertEqual(result["state"], "validated_draft")
        self.assertTrue(result["requires_content_review"])
        # Validating a supplied string is not evidence of an HTTP model call.
        self.assertFalse(result["model_call_performed"])

    def test_unknown_source_or_forged_quote_rejected(self):
        for citation in [{"material_id": "other-course", "quote": "1 km/h"},
                         {"material_id": "units", "quote": "错误的换算"}]:
            with self.subTest(citation=citation):
                with self.assertRaises(ValueError):
                    validate_response(self.rag(), self.response(citations=[citation]))

    def test_rag_explanation_requires_citation(self):
        with self.assertRaises(ValueError):
            validate_response(self.rag(), self.response(citations=[]))

    def test_direct_route_cannot_invent_reference(self):
        direct = plan_answer("半径3cm的圆面积", "math", self.data)
        with self.assertRaises(ValueError):
            validate_response(direct, self.response())
        result = validate_response(direct, self.response(citations=[]))
        self.assertEqual(result["route"], "direct")

    def test_invalid_structure_and_action_rejected(self):
        for raw in ["[]", "invalid-json", self.response(reply=42),
                    self.response(next_action="delete_course"), self.response(citations="units")]:
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):
                    validate_response(self.rag(), raw)

    def test_model_response_cannot_be_attached_to_curated_route(self):
        with self.assertRaises(ValueError):
            validate_response(plan_answer("解不等式 2x+3>7", "math", self.data), self.response())


if __name__ == "__main__":
    unittest.main()
