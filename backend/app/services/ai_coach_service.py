from __future__ import annotations

from sqlalchemy.orm import Session

from app.memory.learner_memory import get_learner_weaknesses
from app.models.coach_memory import CoachMemory
from app.models.error_pattern import ErrorPattern
from app.schemas.learning_path import LearningPathResponse
from app.services.analytics_service import get_user_analytics, get_recent_attempts
from app.services.adaptive_practice_service import (
    get_adaptive_practice_recommendation,
)
from app.services.learning_path_service import get_learning_path


SUGGESTED_QUESTIONS = [
    "What should I practice today?",
    "Why is my speaking score low?",
    "How can I improve vocabulary?",
    "What is my weakest skill?",
    "Create a study plan for this week.",
    "Explain my recent mistakes.",
]
def _summarize_recent_mistakes(db: Session, learner_id: int) -> str:
    patterns = (
        db.query(ErrorPattern)
        .filter(ErrorPattern.learner_id == learner_id)
        .order_by(ErrorPattern.occurrence_count.desc())
        .limit(2)
        .all()
    )
    if not patterns:
        return "I do not see recurring mistakes yet. Keep practicing and I will track the patterns."
    parts = [
        f"{pattern.category} errors are appearing {max(pattern.occurrence_count - pattern.resolved_count, 0)} times"
        for pattern in patterns
    ]
    return " and ".join(parts)


def _build_reply(message: str, analytics: dict, learning_path: LearningPathResponse, recent_attempts: list[dict], mistakes: str) -> str:
    weak = learning_path.weak_skills[0] if learning_path.weak_skills else learning_path.current_focus
    strong = learning_path.strong_skills[0] if learning_path.strong_skills else "your current strengths"
    if "today" in message.lower():
        return (
            f"Based on your recent {weak} results, I recommend one {learning_path.recommended_practice} session and one {learning_path.current_focus} review today. "
            f"Your strongest area is {strong}, so keep it warm with a short review, but spend most of your energy on {weak}. "
            f"Your current level is {learning_path.current_level}, and the next milestone is {learning_path.next_milestone}."
        )
    if "speaking" in message.lower():
        speaking = analytics.get("speaking_accuracy", 0)
        if speaking < 60:
            return (
                f"Your speaking score is {speaking:.0f}, so I want you to do short daily speaking drills. "
                f"Focus on pronunciation, fluency, and confidence. Pair that with one recorded answer and review it after each attempt."
            )
        return (
            f"Your speaking score is {speaking:.0f}, which is fairly stable. "
            f"To keep improving, add one speaking practice session to your weekly plan and review the latest feedback notes."
        )
    if "vocabulary" in message.lower():
        vocab = analytics.get("vocabulary_accuracy", 0)
        if vocab >= 70 and learning_path.recommended_practice.lower() == "vocabulary":
            return (
                f"Your vocabulary is improving quickly at {vocab:.0f}, so I would increase the difficulty slightly. "
                f"Try harder words and use them in both reading and speaking practice."
            )
        return (
            f"Your vocabulary accuracy is {vocab:.0f}. Build it with spaced repetition, short review sessions, and one focused vocabulary set today."
        )
    if "weakest" in message.lower():
        return f"Your weakest skill right now is {learning_path.current_focus}. {mistakes}"
    if "study plan" in message.lower():
        return (
            f"Here is a simple weekly plan: 2 Reading sessions, 2 {learning_path.current_focus} sessions, 1 Vocabulary session, and 1 review day. "
            f"Keep your strongest skill warm with a short recap, but protect your energy for the weaker areas."
        )
    if "mistake" in message.lower():
        return f"Your recent mistakes show a pattern: {mistakes} I would review those before starting the next practice."
    return (
        f"Your current level is {learning_path.current_level}. Focus on {learning_path.current_focus} first, then {learning_path.recommended_practice}. "
        f"Stay consistent and the next milestone is {learning_path.next_milestone}."
    )


def _store_memory(
    db: Session,
    learner_id: int,
    user_message: str,
    reply: str,
    learning_path: LearningPathResponse,
) -> None:
    db.add(
        CoachMemory(
            learner_id=learner_id,
            role="user",
            message=user_message,
            summary=None,
            current_focus=learning_path.current_focus,
            previous_recommendation=learning_path.recommended_practice,
        )
    )
    db.add(
        CoachMemory(
            learner_id=learner_id,
            role="assistant",
            message=reply,
            summary=reply[:500],
            current_focus=learning_path.current_focus,
            previous_recommendation=learning_path.recommended_practice,
        )
    )
    db.commit()


def _conversation_history(db: Session, learner_id: int) -> list[dict]:
    entries = (
        db.query(CoachMemory)
        .filter(CoachMemory.learner_id == learner_id)
        .order_by(CoachMemory.created_at.desc())
        .limit(12)
        .all()
    )
    return [
        {
            "role": entry.role,
            "message": entry.message,
            "summary": entry.summary,
            "current_focus": entry.current_focus,
            "previous_recommendation": entry.previous_recommendation,
            "created_at": entry.created_at.isoformat(),
        }
        for entry in reversed(entries)
    ]


def chat_with_coach(db: Session, learner_id: int, message: str) -> dict:
    analytics = get_user_analytics(db=db, learner_id=learner_id)
    learning_path = get_learning_path(db=db, learner_id=learner_id)
    recommendation = get_adaptive_practice_recommendation(
        db=db,
        learner_id=learner_id,
    )
    recent_attempts = get_recent_attempts(db=db, learner_id=learner_id)
    weaknesses = get_learner_weaknesses(db=db, learner_id=learner_id)
    mistakes = _summarize_recent_mistakes(db, learner_id)
    reply = _build_reply(message, analytics, learning_path, recent_attempts, mistakes)
    if "today" in message.lower():
        reply = (
            f"{reply} Today's adaptive recommendation is {recommendation['recommendedPractice']} at {recommendation['difficulty']} level for about {recommendation['estimatedTime']}."
        )
    _store_memory(db, learner_id, message, reply, learning_path)
    history = _conversation_history(db, learner_id)
    learner_summary = {
        "current_level": learning_path.current_level,
        "overall_progress": learning_path.overall_progress,
        "current_focus": learning_path.current_focus,
        "recommended_practice": learning_path.recommended_practice,
        "weak_skills": learning_path.weak_skills,
        "strong_skills": learning_path.strong_skills,
        "recent_practices": recent_attempts[:3],
        "average_score": analytics.get("average_score", 0),
    }
    return {
        "reply": reply,
        "conversation_history": history,
        "suggested_questions": SUGGESTED_QUESTIONS,
        "current_learner_summary": learner_summary,
        "recommended_next_action": {
            "title": f"Practice {recommendation['recommendedPractice']}",
            "description": recommendation["reason"],
        },
        "weak_skills": [w.category.title() for w in weaknesses[:2]],
        "strong_skills": learning_path.strong_skills,
        "current_learning_path": learning_path.model_dump(),
    }
