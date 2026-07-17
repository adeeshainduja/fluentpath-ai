import json
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.practice_attempt import PracticeAttempt
from app.models.practice_task import PracticeTask
from app.models.progress_metric import ProgressMetric


READING_SAMPLE = {
    "passage_id": "reading-sample-01",
    "passage": {
        "title": "A Sunday at the Community Garden",
        "text": (
            "On Sunday morning, Lina walked to the community garden with her brother.\n"
            "They watered the tomato plants, pulled out weeds, and met two neighbors who were planting basil.\n"
            "After an hour of work, the garden looked cleaner and brighter than before.\n"
            "Lina left feeling proud because she had helped the neighborhood grow."
        ),
    },
    "estimated_minutes": 8,
    "questions": [
        {
            "id": 1,
            "question": "Where did Lina go on Sunday morning?",
            "options": [
                "The community garden",
                "The movie theater",
                "The train station",
                "The supermarket",
            ],
            "answer": "The community garden",
            "explanation": "The passage says Lina walked to the community garden with her brother.",
        },
        {
            "id": 2,
            "question": "What did Lina and her brother do first?",
            "options": [
                "Watered the tomato plants",
                "Pulled out weeds",
                "Bought fresh vegetables",
                "Built a fence",
            ],
            "answer": "Watered the tomato plants",
            "explanation": "Watering the tomato plants is listed before the other garden tasks.",
        },
        {
            "id": 3,
            "question": "Who did they meet at the garden?",
            "options": [
                "Two neighbors planting basil",
                "A teacher and a student",
                "A bus driver and a chef",
                "Three tourists taking photos",
            ],
            "answer": "Two neighbors planting basil",
            "explanation": "The passage mentions two neighbors who were planting basil.",
        },
        {
            "id": 4,
            "question": "How did the garden look after their work?",
            "options": [
                "Cleaner and brighter",
                "Dirty and crowded",
                "Empty and quiet",
                "Smaller and darker",
            ],
            "answer": "Cleaner and brighter",
            "explanation": "The passage says the garden looked cleaner and brighter than before.",
        },
        {
            "id": 5,
            "question": "How did Lina feel at the end?",
            "options": [
                "Proud",
                "Bored",
                "Angry",
                "Tired and upset",
            ],
            "answer": "Proud",
            "explanation": "She left feeling proud because she had helped the neighborhood grow.",
        },
    ],
}


def get_reading_practice() -> dict:
    return READING_SAMPLE


def submit_reading_practice(
    db: Session,
    learner_id: int,
    passage_id: str,
    answers: dict[int, str],
) -> dict:
    if passage_id != READING_SAMPLE["passage_id"]:
        raise ValueError("Reading passage not found")

    questions = READING_SAMPLE["questions"]
    correct_answers = {
        question["id"]: question["answer"]
        for question in questions
    }
    explanations = {
        question["id"]: question["explanation"]
        for question in questions
    }
    user_answers = {
        question["id"]: answers.get(question["id"], "")
        for question in questions
    }

    correct_count = sum(
        1
        for question_id, correct_answer in correct_answers.items()
        if user_answers.get(question_id) == correct_answer
    )

    score = round((correct_count / len(questions)) * 100)

    task = PracticeTask(
        learner_id=learner_id,
        target_skill="reading",
        practice_type="reading",
        difficulty="beginner",
        title=READING_SAMPLE["passage"]["title"],
        instruction="Read the passage and answer the comprehension questions.",
        status="completed",
        strategy="reading_comprehension",
    )
    db.add(task)
    db.flush()

    attempt_payload = {
        "passage_id": passage_id,
        "passage_title": READING_SAMPLE["passage"]["title"],
        "answers": user_answers,
        "correct_answers": correct_answers,
        "score": score,
        "submitted_at": datetime.utcnow().isoformat(),
    }

    attempt = PracticeAttempt(
        learner_id=learner_id,
        task_id=task.id,
        text=json.dumps(attempt_payload),
        practice_type="reading",
    )
    db.add(attempt)
    db.flush()

    db.add(
        ProgressMetric(
            learner_id=learner_id,
            task_id=task.id,
            attempt_id=attempt.id,
            target_skill="reading",
            task_score=score,
            grammar_score=0,
            vocabulary_score=0,
            fluency_score=0,
            pronunciation_score=0,
            response_length=sum(
                1 for answer in user_answers.values() if answer
            ),
            relevant=True,
            sufficient_detail=correct_count >= 3,
            target_skill_practiced=True,
        )
    )

    db.commit()
    db.refresh(attempt)

    return {
        "attempt_id": attempt.id,
        "score": score,
        "correct_answers": correct_answers,
        "explanations": explanations,
        "feedback": _build_feedback(score),
        "user_answers": user_answers,
    }


def _build_feedback(score: int) -> str:
    if score >= 80:
        return "Excellent reading comprehension. You identified the key details accurately."
    if score >= 60:
        return "Good work. You understood most of the passage, and a quick review will help you improve further."
    return "Keep practicing. Re-read the passage carefully and look for the exact details that answer each question."
