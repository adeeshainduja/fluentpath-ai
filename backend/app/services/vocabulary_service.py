import json
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.evaluation_records import VocabularyProgress
from app.models.practice_attempt import PracticeAttempt
from app.models.practice_task import PracticeTask
from app.models.progress_metric import ProgressMetric


VOCABULARY_SAMPLE = {
    "sessionId": 1,
    "difficulty": "Intermediate",
    "questions": [
        {
            "id": 1,
            "word": "Abandon",
            "question": "Choose the correct meaning.",
            "options": [
                "Leave behind",
                "Collect",
                "Protect",
                "Repair",
            ],
            "answer": "Leave behind",
            "explanation": "To abandon something means to leave it behind or give it up.",
        },
        {
            "id": 2,
            "word": "Expand",
            "question": "Choose the correct meaning.",
            "options": [
                "Become larger",
                "Become quieter",
                "Become shorter",
                "Become weaker",
            ],
            "answer": "Become larger",
            "explanation": "Expand means to grow or become larger.",
        },
        {
            "id": 3,
            "word": "Careful",
            "question": "Choose the correct meaning.",
            "options": [
                "Showing attention to avoid mistakes",
                "Full of noise",
                "Hard to understand",
                "Ready to sleep",
            ],
            "answer": "Showing attention to avoid mistakes",
            "explanation": "Careful describes someone who pays close attention and avoids errors.",
        },
        {
            "id": 4,
            "word": "Bright",
            "question": "Choose the correct meaning.",
            "options": [
                "Full of light or intelligence",
                "Very heavy",
                "Completely empty",
                "A little cold",
            ],
            "answer": "Full of light or intelligence",
            "explanation": "Bright can mean full of light or quick to understand.",
        },
    ],
}


def get_vocabulary_practice() -> dict:
    return VOCABULARY_SAMPLE


def submit_vocabulary_practice(
    db: Session,
    learner_id: int,
    session_id: int,
    answers: list[dict],
) -> dict:
    if session_id != VOCABULARY_SAMPLE["sessionId"]:
        raise ValueError("Vocabulary practice not found")

    questions = VOCABULARY_SAMPLE["questions"]
    correct_answers = {
        question["id"]: question["answer"]
        for question in questions
    }
    explanations = {
        question["id"]: question["explanation"]
        for question in questions
    }
    answer_lookup = {
        item["question_id"]: item["selected_option"]
        for item in answers
    }

    correct_count = sum(
        1
        for question_id, correct_answer in correct_answers.items()
        if answer_lookup.get(question_id) == correct_answer
    )
    score = round((correct_count / len(questions)) * 100)

    task = PracticeTask(
        learner_id=learner_id,
        target_skill="vocabulary",
        practice_type="vocabulary",
        difficulty=VOCABULARY_SAMPLE["difficulty"].lower(),
        title="Vocabulary Practice",
        instruction="Choose the correct meaning for each word.",
        status="completed",
        strategy="vocabulary_matching",
    )
    db.add(task)
    db.flush()

    attempt_payload = {
        "sessionId": session_id,
        "difficulty": VOCABULARY_SAMPLE["difficulty"],
        "answers": answer_lookup,
        "correct_answers": correct_answers,
        "score": score,
        "submitted_at": datetime.utcnow().isoformat(),
    }

    attempt = PracticeAttempt(
        learner_id=learner_id,
        task_id=task.id,
        text=json.dumps(attempt_payload),
        practice_type="vocabulary",
    )
    db.add(attempt)
    db.flush()

    for question in questions:
        word = question["word"]
        progress = (
            db.query(VocabularyProgress)
            .filter(
                VocabularyProgress.user_id == learner_id,
                VocabularyProgress.word == word,
            )
            .first()
        )

        if progress is None:
            progress = VocabularyProgress(
                user_id=learner_id,
                word=word,
                mastery_level=0,
                times_practiced=0,
                last_practiced_at=None,
            )
            db.add(progress)

        if answer_lookup.get(question["id"]) == question["answer"]:
            progress.mastery_level = min(progress.mastery_level + 20, 100)
        else:
            progress.mastery_level = min(progress.mastery_level + 5, 100)

        progress.times_practiced += 1
        progress.last_practiced_at = datetime.utcnow()

    db.add(
        ProgressMetric(
            learner_id=learner_id,
            task_id=task.id,
            attempt_id=attempt.id,
            target_skill="vocabulary",
            task_score=score,
            grammar_score=0,
            vocabulary_score=score,
            fluency_score=0,
            pronunciation_score=0,
            response_length=len(answer_lookup),
            relevant=True,
            sufficient_detail=correct_count >= 3,
            target_skill_practiced=True,
        )
    )

    db.commit()
    db.refresh(attempt)

    return {
        "score": score,
        "correct_answers": correct_answers,
        "explanations": explanations,
        "feedback": _build_feedback(score),
    }


def _build_feedback(score: int) -> str:
    if score >= 80:
        return "Good vocabulary knowledge."
    if score >= 60:
        return "Solid progress. Review the words you missed and try again."
    return "Keep practicing. Focus on the core meaning of each word and check the options carefully."
