import sys
import unittest
import json
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'examples'))
from core import retrieve, validate_qa_response, route_photo, validate_grade, publish_grade
from model_client import parse_model_object


class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.documents = [
            {'id': 'math-factor', 'course_id': 'math-demo', 'status': 'approved',
             'text': '二次方程因式分解：x^2-5x+6=(x-2)(x-3)。'},
            {'id': 'other-course', 'course_id': 'other', 'status': 'approved',
             'text': '二次方程因式分解：跨课程测试材料。'},
            {'id': 'unreviewed', 'course_id': 'math-demo', 'status': 'draft',
             'text': '二次方程因式分解：未审核材料。'},
        ]

    def test_returns_relevant_approved_course_evidence(self):
        results = retrieve('二次方程怎么因式分解', self.documents, 'math-demo')
        self.assertEqual([item['id'] for item in results], ['math-factor'])

    def test_does_not_leak_a_matching_document_from_another_course(self):
        results = retrieve('二次方程', self.documents, 'other')
        self.assertEqual([item['id'] for item in results], ['other-course'])

    def test_unrelated_question_produces_no_evidence(self):
        self.assertEqual(retrieve('蛋白质合成过程', self.documents, 'math-demo'), [])


class CitationTests(unittest.TestCase):
    def setUp(self):
        self.documents = [{'id': 'factor', 'course_id': 'math-demo',
                           'status': 'approved', 'text': '因式分解得到 (x-2)(x-3)=0。'}]
        self.response = {'answer': '先把左边因式分解。', 'next_action': 'answer',
                         'citations': [{'document_id': 'factor', 'quote': '(x-2)(x-3)=0'}]}

    def test_rejects_fabricated_document_reference(self):
        self.response['citations'][0]['document_id'] = 'does-not-exist'
        with self.assertRaises(ValueError):
            validate_qa_response(self.response, self.documents, 'math-demo')

    def test_rejects_non_string_document_reference(self):
        self.response['citations'][0]['document_id'] = []
        with self.assertRaises(ValueError):
            validate_qa_response(self.response, self.documents, 'math-demo')

    def test_rejects_a_quote_missing_from_the_actual_document(self):
        self.response['citations'][0]['quote'] = 'x=6'
        with self.assertRaises(ValueError):
            validate_qa_response(self.response, self.documents, 'math-demo')

    def test_rejects_an_answer_without_evidence(self):
        self.response['citations'] = []
        with self.assertRaises(ValueError):
            validate_qa_response(self.response, self.documents, 'math-demo')

    def test_rejects_cross_course_citation(self):
        with self.assertRaises(ValueError):
            validate_qa_response(self.response, self.documents, 'other')

    def test_allows_a_teacher_escalation_without_evidence(self):
        result = validate_qa_response({'answer': '请教师补充材料。', 'citations': [],
                                      'next_action': 'teacher_review'}, [], 'math-demo')
        self.assertEqual(result['next_action'], 'teacher_review')


class PhotoTests(unittest.TestCase):
    def setUp(self):
        self.bank = [{'id': 'quadratic-01', 'course_id': 'math-demo', 'status': 'approved',
                      'text': '解方程 x^2-5x+6=0', 'answer': 'x=2 或 x=3'}]

    def test_routes_uncertain_minus_sign_to_confirmation(self):
        result = route_photo({'text': '解方程 x^2-5x+6=0',
                              'uncertain_regions': ['5x 前符号模糊']}, self.bank)
        self.assertEqual(result['status'], 'ask_confirmation')

    def test_matches_supported_superscript_and_spacing_normalization(self):
        result = route_photo({'text': '解方程 x² − 5x + 6 = 0', 'uncertain_regions': []}, self.bank)
        self.assertEqual(result['status'], 'exact_match')
        self.assertEqual(result['question_id'], 'quadratic-01')
        self.assertTrue(result['requires_visual_confirmation'])

    def test_does_not_match_a_different_plus_sign(self):
        result = route_photo({'text': '解方程 x^2+5x+6=0', 'uncertain_regions': []}, self.bank)
        self.assertEqual(result['status'], 'teacher_review')


class GradingTests(unittest.TestCase):
    def setUp(self):
        self.rubric = [{'id': 'C1', 'max_score': 2}, {'id': 'C2', 'max_score': 2},
                       {'id': 'C3', 'max_score': 1}]
        self.answer = '(x-2)(x-3)=0，所以 x=2。'
        self.proposal = {'scores': [
            {'criterion_id': 'C1', 'score': 2, 'quote': '(x-2)(x-3)=0', 'reason': '分解正确'},
            {'criterion_id': 'C2', 'score': 1, 'quote': 'x=2', 'reason': '只写一个根'},
            {'criterion_id': 'C3', 'score': 0, 'quote': '', 'reason': '未代入检验'},
        ]}

    def test_computes_partial_credit_and_requires_teacher_review(self):
        result = validate_grade(self.proposal, self.answer, self.rubric)
        self.assertEqual(result['total'], 3)
        self.assertEqual(result['status'], 'teacher_review')

    def test_rejects_score_above_rubric_maximum(self):
        self.proposal['scores'][0]['score'] = 9
        with self.assertRaises(ValueError):
            validate_grade(self.proposal, self.answer, self.rubric)

    def test_rejects_boolean_as_numeric_score(self):
        self.proposal['scores'][0]['score'] = True
        with self.assertRaises(ValueError):
            validate_grade(self.proposal, self.answer, self.rubric)

    def test_rejects_fractional_score_for_integer_rubric(self):
        self.proposal['scores'][0]['score'] = 1.5
        with self.assertRaises(ValueError):
            validate_grade(self.proposal, self.answer, self.rubric)

    def test_rejects_non_string_criterion_with_validation_error(self):
        self.proposal['scores'][0]['criterion_id'] = []
        with self.assertRaises(ValueError):
            validate_grade(self.proposal, self.answer, self.rubric)

    def test_rejects_evidence_not_present_in_student_work(self):
        self.proposal['scores'][1]['quote'] = 'x=3'
        with self.assertRaises(ValueError):
            validate_grade(self.proposal, self.answer, self.rubric)

    def test_rejects_duplicate_criterion_that_inflates_total(self):
        self.proposal['scores'].append(self.proposal['scores'][0].copy())
        with self.assertRaises(ValueError):
            validate_grade(self.proposal, self.answer, self.rubric)

    def test_never_publishes_without_teacher_approval(self):
        result = validate_grade(self.proposal, self.answer, self.rubric)
        with self.assertRaises(ValueError):
            publish_grade(result, approved=False, reviewer='demo-reviewer')

    def test_requires_a_reviewer_and_publication_is_idempotent(self):
        result = validate_grade(self.proposal, self.answer, self.rubric)
        with self.assertRaises(ValueError):
            publish_grade(result, approved=True, reviewer='')
        published = publish_grade(result, approved=True, reviewer='demo-reviewer')
        self.assertEqual(published['status'], 'published')
        self.assertEqual(publish_grade(published, approved=True, reviewer='demo-reviewer'), published)


class ModelBoundaryTests(unittest.TestCase):
    def test_parses_a_structured_response(self):
        self.assertEqual(parse_model_object('{"answer":"test"}').get('answer'), 'test')

    def test_rejects_invalid_json_instead_of_silently_publishing(self):
        with self.assertRaises(ValueError):
            parse_model_object('not JSON')

    def test_rejects_a_top_level_array(self):
        with self.assertRaises(ValueError):
            parse_model_object('[1,2]')


class OfflineCLITests(unittest.TestCase):
    def run_case(self, *args):
        root = Path(__file__).resolve().parents[1]
        proc = subprocess.run([sys.executable, str(root/'examples/run.py'), *args],
                              cwd=root, capture_output=True, text=True, timeout=10)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return json.loads(proc.stdout)

    def test_qa_default_returns_evidence_with_no_generated_answer(self):
        result = self.run_case('qa', '--question', '二次方程怎么因式分解')
        self.assertEqual(result['mode'], 'offline_evidence')
        self.assertNotIn('answer', result)
        self.assertTrue(result['evidence'])

    def test_uncertain_photo_requests_confirmation(self):
        result = self.run_case('photo', '--fixture', 'examples/data/photo-uncertain.json')
        self.assertEqual(result['status'], 'ask_confirmation')

    def test_grade_returns_draft_instead_of_published_result(self):
        result = self.run_case('grade', '--fixture', 'examples/data/grade-partial.json')
        self.assertEqual(result['total'], 3)
        self.assertEqual(result['status'], 'teacher_review')


if __name__ == '__main__':
    unittest.main()
