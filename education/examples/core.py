"""Original teaching helpers; offline checks do not measure model accuracy."""
import re
from copy import deepcopy


def retrieve(question, documents, course_id, limit=3):
    text = question.lower()
    terms = set(re.findall(r'[a-z0-9]+', text))
    for segment in re.findall(r'[\u4e00-\u9fff]+', text):
        terms.update(segment[i:i + 2] for i in range(len(segment) - 1))
    if not terms:
        return []
    results = []
    for document in documents:
        if document.get('course_id') != course_id or document.get('status') != 'approved':
            continue
        content = document['text'].lower()
        doc_terms = set(re.findall(r'[a-z0-9]+', content))
        for segment in re.findall(r'[\u4e00-\u9fff]+', content):
            doc_terms.update(segment[i:i + 2] for i in range(len(segment) - 1))
        score = len(terms & doc_terms) / len(terms)
        if score:
            results.append({**document, 'lexical_overlap': round(score, 4)})
    return sorted(results, key=lambda item: (-item['lexical_overlap'], item['id']))[:limit]


def validate_qa_response(response, documents, course_id):
    if not isinstance(response, dict) or not isinstance(response.get('answer'), str):
        raise ValueError('answer must be a string')
    action = response.get('next_action')
    citations = response.get('citations')
    if action not in ('answer', 'teacher_review') or not isinstance(citations, list):
        raise ValueError('invalid next_action or citations')
    permitted = {doc['id']: doc for doc in documents
                 if doc.get('course_id') == course_id and doc.get('status') == 'approved'}
    if action == 'answer' and (not citations or not response['answer'].strip()):
        raise ValueError('answer requires text and evidence')
    for citation in citations:
        if not isinstance(citation, dict):
            raise ValueError('citation must be an object')
        document_id = citation.get('document_id')
        if not isinstance(document_id, str):
            raise ValueError('document_id must be a string')
        doc = permitted.get(document_id)
        quote = citation.get('quote')
        if not doc or not isinstance(quote, str) or not quote.strip() or quote not in doc['text']:
            raise ValueError('citation is unavailable or quote is not literal source text')
    return deepcopy(response)


def route_photo(observation, question_bank, course_id='math-demo'):
    if not isinstance(observation, dict) or not isinstance(observation.get('text'), str):
        raise ValueError('transcription text must be a string')
    uncertain = observation.get('uncertain_regions')
    if not isinstance(uncertain, list) or any(not isinstance(item, str) for item in uncertain):
        raise ValueError('uncertain_regions must be a list of strings')
    if uncertain or not observation['text'].strip():
        return {'status': 'ask_confirmation', 'text': observation['text'],
                'uncertain_regions': uncertain}
    def normalized(text):
        return re.sub(r'\s+', '', text).replace('²', '^2').replace('−', '-')
    matches = [item for item in question_bank
               if item.get('course_id') == course_id and item.get('status') == 'approved'
               and normalized(item['text']) == normalized(observation['text'])]
    if len(matches) != 1:
        return {'status': 'teacher_review', 'text': observation['text']}
    return {'status': 'exact_match', 'question_id': matches[0]['id'],
            'matched_text': matches[0]['text'], 'candidate_answer': matches[0]['answer'],
            'requires_visual_confirmation': True}


def validate_grade(proposal, student_answer, rubric):
    if not isinstance(proposal, dict) or not isinstance(proposal.get('scores'), list):
        raise ValueError('scores must be a list')
    if not isinstance(student_answer, str):
        raise ValueError('student answer must be text')
    criteria = {item['id']: item for item in rubric}
    seen = set()
    total = 0
    for item in proposal['scores']:
        if not isinstance(item, dict):
            raise ValueError('score item must be an object')
        criterion_id = item.get('criterion_id')
        if not isinstance(criterion_id, str) or criterion_id not in criteria or criterion_id in seen:
            raise ValueError('unknown or duplicate criterion')
        seen.add(criterion_id)
        score, quote, reason = item.get('score'), item.get('quote'), item.get('reason')
        if type(score) is not int:
            raise ValueError('score must be an integer, not a boolean or fractional number')
        if not 0 <= score <= criteria[criterion_id]['max_score']:
            raise ValueError('score exceeds rubric range')
        if not isinstance(quote, str) or (score > 0 and not quote.strip()):
            raise ValueError('positive score requires literal student evidence')
        if quote and quote not in student_answer:
            raise ValueError('evidence not present in student answer')
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError('reason must be nonempty text')
        total += score
    if seen != set(criteria):
        raise ValueError('every criterion must appear exactly once')
    return {'scores': deepcopy(proposal['scores']), 'total': total,
            'max_score': sum(item['max_score'] for item in rubric), 'status': 'teacher_review'}


def publish_grade(draft, approved=False, reviewer=None):
    # Demonstrates a state gate, not authentication or durable transaction handling.
    if draft.get('status') == 'published':
        return deepcopy(draft)
    if draft.get('status') != 'teacher_review' or approved is not True:
        raise ValueError('teacher approval required')
    if not isinstance(reviewer, str) or not reviewer.strip():
        raise ValueError('reviewer required')
    return {**deepcopy(draft), 'status': 'published', 'reviewer': reviewer}
