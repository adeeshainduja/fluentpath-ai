import json
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.evaluation_records import ListeningEvaluation
from app.models.practice_attempt import PracticeAttempt
from app.models.practice_task import PracticeTask
from app.models.progress_metric import ProgressMetric


LISTENING_SAMPLE = {
    "practice_id": "listening-sample-01",
    "audio_url": "/audio/listening-sample.mp3",
    "transcript": (
        "Good morning everyone. The library workshop will start at 10 a.m. in Room 3. "
        "Please bring a notebook and a pen. After the workshop, visitors can join a short question session."
    ),
    "estimated_minutes": 7,
    "questions": [
        {
            "id": 1,
            "question": "When will the workshop start?",
            "options": [
                "10 a.m.",
                "9 a.m.",
                "11 a.m.",
                "12 p.m.",
            ],
            "answer": "10 a.m.",
            "explanation": "The transcript says the workshop will start at 10 a.m.",
        },
        {
            "id": 2,
            "question": "Where will the workshop take place?",
            "options": [
                "Room 3",
                "Room 1",
                "The lobby",
                "The cafeteria",
            ],
            "answer": "Room 3",
            "explanation": "The transcript mentions Room 3 as the location.",
        },
        {
            "id": 3,
            "question": "What should visitors bring?",
            "options": [
                "A notebook and a pen",
                "A laptop and charger",
                "A camera and bag",
                "A water bottle only",
            ],
            "answer": "A notebook and a pen",
            "explanation": "The transcript instructs visitors to bring a notebook and a pen.",
        },
        {
            "id": 4,
            "question": "What happens after the workshop?",
            "options": [
                "A short question session",
                "A lunch break",
                "A second workshop",
                "A group photo only",
            ],
            "answer": "A short question session",
            "explanation": "The transcript says visitors can join a short question session after the workshop.",
        },
        {
            "id": 5,
            "question": "Which place is mentioned in the transcript?",
            "options": [
                "The library",
                "The airport",
                "The stadium",
                "The beach",
            ],
            "answer": "The library",
            "explanation": "The workshop is announced by the library.",
        },
    ],
}


def get_listening_practice() -> dict:
    return LISTENING_SAMPLE


def submit_listening_practice(
    db: Session,
    learner_id: int,
    practice_id: str,
    answers: dict[int, str],
) -> dict:
    if practice_id != LISTENING_SAMPLE["practice_id"]:
        raise ValueError("Listening practice not found")

    questions = LISTENING_SAMPLE["questions"]
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
    ai_feedback = _build_feedback(score)

    task = PracticeTask(
        learner_id=learner_id,
        target_skill="listening",
        practice_type="listening",
        difficulty="beginner",
        title="Library Workshop Announcement",
        instruction="Listen to the audio and answer the comprehension questions.",
        status="completed",
        strategy="listening_comprehension",
    )
    db.add(task)
    db.flush()

    attempt_payload = {
        "practice_id": practice_id,
        "audio_url": LISTENING_SAMPLE["audio_url"],
        "transcript": LISTENING_SAMPLE["transcript"],
        "answers": user_answers,
        "correct_answers": correct_answers,
        "score": score,
        "submitted_at": datetime.utcnow().isoformat(),
    }

    attempt = PracticeAttempt(
        learner_id=learner_id,
        task_id=task.id,
        text=json.dumps(attempt_payload),
        practice_type="listening",
    )
    db.add(attempt)
    db.flush()

    db.add(
        ListeningEvaluation(
            user_id=learner_id,
            prompt=LISTENING_SAMPLE["transcript"],
            response=json.dumps(user_answers),
            score=score,
            result={
                "practice_id": practice_id,
                "correct_answers": correct_answers,
                "explanations": explanations,
                "feedback": ai_feedback,
            },
        )
    )

    db.add(
        ProgressMetric(
            learner_id=learner_id,
            task_id=task.id,
            attempt_id=attempt.id,
            target_skill="listening",
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
        "feedback": ai_feedback,
        "ai_feedback": ai_feedback,
        "user_answers": user_answers,
        "transcript": LISTENING_SAMPLE["transcript"],
        "audio_url": LISTENING_SAMPLE["audio_url"],
    }


def _build_feedback(score: int) -> str:
    if score >= 80:
        return "Excellent listening comprehension. You captured the important details accurately."
    if score >= 60:
        return "Good work. You understood the main idea and most details, and a quick review will help even more."
    return "Keep practicing. Listen for time, place, and action words to identify the key details."
