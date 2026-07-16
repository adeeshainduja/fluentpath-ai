from collections import defaultdict
from datetime import datetime, timedelta
from statistics import pstdev

from sqlalchemy.orm import Session

from app.models.error_pattern import ErrorPattern
from app.schemas.learner_intelligence import (
    AdaptiveLearningPath,
    DashboardInsights,
    LearnerIntelligenceResponse,
    LearnerPerformanceAnalysis,
    LearnerRecommendation,
    LearnerRecommendations,
    LearnerStrengths,
    LearnerWeaknesses,
    LearningGoal,
    PracticeFrequency,
    ScoreTrendPoint,
    SkillAverage,
    StrengthInsight,
    WeaknessInsight,
)
from app.schemas.practice_history import PracticeHistoryItem
from app.services.practice_history_service import (
    get_practice_history_items,
)


SCORE_FIELDS = {
    "grammar": "grammar_score",
    "vocabulary": "vocabulary_score",
    "fluency": "fluency_score",
    "pronunciation": "pronunciation_score",
    "confidence": "confidence_score",
}


def _score_trend(scores: list[int]) -> str:
    if len(scores) < 2:
        return "not_enough_data"

    change = scores[-1] - scores[0]

    if change >= 8:
        return "improving"

    if change <= -8:
        return "declining"

    return "stable"


def _severity(score: float | None) -> str:
    if score is None:
        return "unknown"

    if score < 50:
        return "high"

    if score < 70:
        return "medium"

    return "low"


def _priority_from_score(
    score: float | None,
    trend: str = "stable",
) -> int:
    if score is None:
        base_priority = 45
    else:
        base_priority = round(100 - score)

    if trend == "declining":
        base_priority += 15
    elif trend == "improving":
        base_priority -= 10

    return max(
        0,
        min(100, base_priority),
    )


def _practice_type_for_skill(
    skill: str,
) -> str:
    if skill in {
        "pronunciation",
        "fluency",
        "confidence",
    }:
        return "speaking"

    return "writing"


def _current_level(
    average_score: float | None,
) -> str:
    if average_score is None:
        return "Unassessed"

    if average_score >= 90:
        return "C2"
    if average_score >= 80:
        return "C1"
    if average_score >= 70:
        return "B2"
    if average_score >= 60:
        return "B1"
    if average_score >= 45:
        return "A2"

    return "A1"


def _active_streak(
    items: list[PracticeHistoryItem],
) -> int:
    practice_days = sorted(
        {
            item.created_at.date()
            for item in items
        },
        reverse=True,
    )

    if not practice_days:
        return 0

    streak = 1
    current_day = practice_days[0]

    for next_day in practice_days[1:]:
        if current_day - next_day == timedelta(days=1):
            streak += 1
            current_day = next_day
        else:
            break

    return streak


def _dimension_scores(
    items: list[PracticeHistoryItem],
) -> dict[str, list[tuple[datetime, int]]]:
    grouped: dict[str, list[tuple[datetime, int]]] = {
        skill: []
        for skill in SCORE_FIELDS
    }

    for item in sorted(
        items,
        key=lambda history_item: history_item.created_at,
    ):
        for skill, field_name in SCORE_FIELDS.items():
            score = getattr(item, field_name)

            if score is not None:
                grouped[skill].append(
                    (
                        item.created_at,
                        score,
                    )
                )

    return grouped


def _target_skill_scores(
    items: list[PracticeHistoryItem],
) -> dict[str, list[tuple[datetime, int]]]:
    grouped: dict[str, list[tuple[datetime, int]]] = defaultdict(list)

    for item in sorted(
        items,
        key=lambda history_item: history_item.created_at,
    ):
        if item.target_skill and item.score is not None:
            grouped[item.target_skill].append(
                (
                    item.created_at,
                    item.score,
                )
            )

    return grouped


def _average_skill_scores(
    items: list[PracticeHistoryItem],
) -> list[SkillAverage]:
    grouped = _dimension_scores(items)
    grouped.update(_target_skill_scores(items))

    skill_averages: list[SkillAverage] = []

    for skill, values in grouped.items():
        if not values:
            continue

        scores = [
            score
            for _, score in values
        ]

        skill_averages.append(
            SkillAverage(
                skill=skill,
                average_score=round(
                    sum(scores) / len(scores),
                    2,
                ),
                attempts=len(scores),
                latest_score=scores[-1],
                trend=_score_trend(scores),
            )
        )

    return sorted(
        skill_averages,
        key=lambda item: item.average_score,
    )


def analyze_performance(
    db: Session,
    learner_id: int,
) -> LearnerPerformanceAnalysis:
    items = get_practice_history_items(
        db=db,
        learner_id=learner_id,
    )

    chronological_items = sorted(
        items,
        key=lambda item: item.created_at,
    )

    scored_items = [
        item
        for item in chronological_items
        if item.score is not None
    ]

    scores = [
        item.score
        for item in scored_items
        if item.score is not None
    ]

    active_days = {
        item.created_at.date()
        for item in items
    }

    now = datetime.utcnow()
    last_7_days = now - timedelta(days=7)
    last_30_days = now - timedelta(days=30)

    speaking_trend = [
        ScoreTrendPoint(
            date=item.created_at.date().isoformat(),
            score=item.score,
            practice_type=item.practice_type,
            skill=item.target_skill,
        )
        for item in chronological_items
        if item.source == "speaking_attempt"
        and item.score is not None
    ]

    writing_trend = [
        ScoreTrendPoint(
            date=item.created_at.date().isoformat(),
            score=item.score,
            practice_type=item.practice_type,
            skill=item.target_skill,
        )
        for item in chronological_items
        if item.source == "practice_attempt"
        and item.score is not None
    ]

    improvement_rate = None

    if len(scores) >= 2:
        first_window = scores[: min(5, len(scores))]
        recent_window = scores[-min(5, len(scores)) :]

        improvement_rate = round(
            (
                sum(recent_window) / len(recent_window)
            )
            - (
                sum(first_window) / len(first_window)
            ),
            2,
        )

    consistency = None
    consistency_label = "not_enough_data"

    if len(scores) >= 2:
        consistency = round(
            max(0, 100 - pstdev(scores)),
            2,
        )

        if consistency >= 90:
            consistency_label = "high"
        elif consistency >= 75:
            consistency_label = "moderate"
        else:
            consistency_label = "variable"

    return LearnerPerformanceAnalysis(
        learner_id=learner_id,
        average_scores_by_skill=_average_skill_scores(items),
        speaking_trend=speaking_trend,
        writing_trend=writing_trend,
        practice_frequency=PracticeFrequency(
            total_practices=len(items),
            active_days=len(active_days),
            practices_last_7_days=len(
                [
                    item
                    for item in items
                    if item.created_at >= last_7_days
                ]
            ),
            practices_last_30_days=len(
                [
                    item
                    for item in items
                    if item.created_at >= last_30_days
                ]
            ),
            average_practices_per_active_day=round(
                len(items) / len(active_days),
                2,
            )
            if active_days
            else 0,
            current_streak=_active_streak(items),
        ),
        improvement_rate=improvement_rate,
        consistency=consistency,
        consistency_label=consistency_label,
    )


def _error_pattern_weaknesses(
    db: Session,
    learner_id: int,
) -> list[WeaknessInsight]:
    patterns = (
        db.query(ErrorPattern)
        .filter(
            ErrorPattern.learner_id == learner_id,
        )
        .all()
    )

    weaknesses: list[WeaknessInsight] = []

    for pattern in patterns:
        active_count = max(
            pattern.occurrence_count - pattern.resolved_count,
            0,
        )

        if active_count <= 0:
            continue

        priority = min(
            100,
            50 + active_count * 10,
        )

        weaknesses.append(
            WeaknessInsight(
                skill=pattern.category,
                category=pattern.error_type,
                evidence=(
                    f"{active_count} unresolved "
                    f"{pattern.category.replace('_', ' ')} error"
                    f"{'' if active_count == 1 else 's'}."
                ),
                severity=(
                    "high"
                    if active_count >= 4
                    else "medium"
                ),
                priority=priority,
            )
        )

    return weaknesses


def _score_weaknesses(
    performance: LearnerPerformanceAnalysis,
) -> list[WeaknessInsight]:
    weaknesses: list[WeaknessInsight] = []

    for skill in performance.average_scores_by_skill:
        if skill.average_score >= 75:
            continue

        weaknesses.append(
            WeaknessInsight(
                skill=skill.skill,
                category="score",
                score=skill.average_score,
                evidence=(
                    f"Average score is {skill.average_score} "
                    f"across {skill.attempts} evaluated attempt"
                    f"{'' if skill.attempts == 1 else 's'}."
                ),
                severity=_severity(skill.average_score),
                priority=_priority_from_score(
                    skill.average_score,
                    skill.trend,
                ),
            )
        )

    return weaknesses


def detect_weaknesses(
    db: Session,
    learner_id: int,
) -> LearnerWeaknesses:
    performance = analyze_performance(
        db=db,
        learner_id=learner_id,
    )

    score_weaknesses = _score_weaknesses(
        performance
    )
    error_weaknesses = _error_pattern_weaknesses(
        db=db,
        learner_id=learner_id,
    )

    all_weaknesses = sorted(
        [
            *score_weaknesses,
            *error_weaknesses,
        ],
        key=lambda item: item.priority,
        reverse=True,
    )

    def by_skills(
        *skills: str,
    ) -> list[WeaknessInsight]:
        return [
            item
            for item in all_weaknesses
            if item.skill in skills
            or item.category in skills
        ][:5]

    grammar_topics = [
        item
        for item in all_weaknesses
        if item.skill not in {
            "vocabulary",
            "pronunciation",
            "fluency",
            "confidence",
        }
        and item.category not in {
            "vocabulary",
            "pronunciation",
            "fluency",
            "confidence",
        }
    ][:5]

    return LearnerWeaknesses(
        learner_id=learner_id,
        grammar_topics=grammar_topics,
        vocabulary_weaknesses=by_skills(
            "vocabulary",
            "word_choice",
        ),
        pronunciation_weaknesses=by_skills(
            "pronunciation",
        ),
        fluency_weaknesses=by_skills(
            "fluency",
        ),
        confidence_weaknesses=by_skills(
            "confidence",
        ),
    )


def detect_strengths(
    db: Session,
    learner_id: int,
) -> LearnerStrengths:
    performance = analyze_performance(
        db=db,
        learner_id=learner_id,
    )

    skill_scores = performance.average_scores_by_skill

    highest = [
        StrengthInsight(
            skill=skill.skill,
            category="highest_performance",
            score=skill.average_score,
            evidence=(
                f"Average score is {skill.average_score} "
                f"across {skill.attempts} evaluated attempt"
                f"{'' if skill.attempts == 1 else 's'}."
            ),
        )
        for skill in sorted(
            skill_scores,
            key=lambda item: item.average_score,
            reverse=True,
        )
        if skill.average_score >= 80
    ][:5]

    improved = [
        StrengthInsight(
            skill=skill.skill,
            category="most_improved",
            score=skill.latest_score or skill.average_score,
            evidence=(
                f"{skill.skill.replace('_', ' ').title()} "
                "is trending upward."
            ),
        )
        for skill in skill_scores
        if skill.trend == "improving"
    ][:5]

    consistent = [
        StrengthInsight(
            skill=skill.skill,
            category="consistent_strength",
            score=skill.average_score,
            consistency=performance.consistency,
            evidence=(
                f"{skill.skill.replace('_', ' ').title()} "
                "is strong while overall performance is consistent."
            ),
        )
        for skill in skill_scores
        if skill.average_score >= 75
        and performance.consistency is not None
        and performance.consistency >= 80
    ][:5]

    return LearnerStrengths(
        learner_id=learner_id,
        highest_performing_skills=highest,
        most_improved_skills=improved,
        consistent_strengths=consistent,
    )


def _flatten_weaknesses(
    weaknesses: LearnerWeaknesses,
) -> list[WeaknessInsight]:
    return [
        *weaknesses.grammar_topics,
        *weaknesses.vocabulary_weaknesses,
        *weaknesses.pronunciation_weaknesses,
        *weaknesses.fluency_weaknesses,
        *weaknesses.confidence_weaknesses,
    ]


def generate_recommendations(
    db: Session,
    learner_id: int,
) -> LearnerRecommendations:
    performance = analyze_performance(
        db=db,
        learner_id=learner_id,
    )
    weaknesses = detect_weaknesses(
        db=db,
        learner_id=learner_id,
    )

    recommendations: list[LearnerRecommendation] = []
    seen_skills: set[str] = set()

    for weakness in _flatten_weaknesses(weaknesses):
        if weakness.skill in seen_skills:
            continue

        seen_skills.add(weakness.skill)
        practice_type = _practice_type_for_skill(
            weakness.skill
        )

        recommendations.append(
            LearnerRecommendation(
                recommendation=(
                    "Prioritize "
                    f"{weakness.skill.replace('_', ' ')} "
                    f"through focused {practice_type} practice."
                ),
                reason=weakness.evidence,
                affected_skill=weakness.skill,
                confidence=round(
                    min(0.95, 0.5 + weakness.priority / 200),
                    2,
                ),
                priority=weakness.priority,
                suggested_practice_type=practice_type,
            )
        )

    if (
        performance.practice_frequency.practices_last_7_days < 3
        and performance.practice_frequency.total_practices > 0
    ):
        recommendations.append(
            LearnerRecommendation(
                recommendation=(
                    "Increase weekly practice frequency to "
                    "build retention and fluency."
                ),
                reason=(
                    "The learner completed "
                    f"{performance.practice_frequency.practices_last_7_days} "
                    "practice session(s) in the last 7 days."
                ),
                affected_skill="consistency",
                confidence=0.72,
                priority=70,
                suggested_practice_type="mixed",
            )
        )

    if (
        performance.improvement_rate is not None
        and performance.improvement_rate < 0
    ):
        recommendations.append(
            LearnerRecommendation(
                recommendation=(
                    "Review recent weak areas before increasing "
                    "difficulty."
                ),
                reason=(
                    "Recent average performance dropped by "
                    f"{abs(performance.improvement_rate)} points."
                ),
                affected_skill="overall_progress",
                confidence=0.78,
                priority=min(
                    100,
                    65 + round(abs(performance.improvement_rate)),
                ),
                suggested_practice_type="review",
            )
        )

    recommendations.sort(
        key=lambda item: item.priority,
        reverse=True,
    )

    return LearnerRecommendations(
        learner_id=learner_id,
        recommendations=recommendations[:5],
    )


def generate_learning_path(
    db: Session,
    learner_id: int,
) -> AdaptiveLearningPath:
    performance = analyze_performance(
        db=db,
        learner_id=learner_id,
    )
    recommendations = generate_recommendations(
        db=db,
        learner_id=learner_id,
    )
    strengths = detect_strengths(
        db=db,
        learner_id=learner_id,
    )

    scored_averages = [
        skill.average_score
        for skill in performance.average_scores_by_skill
    ]
    average_score = (
        sum(scored_averages) / len(scored_averages)
        if scored_averages
        else None
    )
    rounded_average = (
        round(average_score, 2)
        if average_score is not None
        else None
    )

    completed_skills = sorted(
        {
            strength.skill
            for strength in [
                *strengths.highest_performing_skills,
                *strengths.consistent_strengths,
            ]
        }
    )

    remaining_skills = [
        recommendation.affected_skill
        for recommendation in recommendations.recommendations
        if recommendation.affected_skill not in completed_skills
    ]

    goals = [
        LearningGoal(
            goal=(
                "Improve "
                f"{recommendation.affected_skill.replace('_', ' ')}"
            ),
            target_skill=recommendation.affected_skill,
            reason=recommendation.reason,
            suggested_practice_type=(
                recommendation.suggested_practice_type
            ),
            priority=recommendation.priority,
            success_metric=(
                "Raise the related average score by at "
                "least 8 points across the next evaluated attempts."
            ),
        )
        for recommendation in recommendations.recommendations
    ]

    return AdaptiveLearningPath(
        learner_id=learner_id,
        current_level=_current_level(average_score),
        progress=rounded_average,
        current_focus=(
            recommendations.recommendations[0].affected_skill
            if recommendations.recommendations
            else None
        ),
        current_goal=(
            goals[0].goal
            if goals
            else None
        ),
        recommended_practice=(
            recommendations.recommendations[0]
            if recommendations.recommendations
            else None
        ),
        completed_skills=completed_skills,
        remaining_skills=remaining_skills,
        goals=goals,
    )


def generate_dashboard_insights(
    db: Session,
    learner_id: int,
) -> DashboardInsights:
    performance = analyze_performance(
        db=db,
        learner_id=learner_id,
    )
    strengths = detect_strengths(
        db=db,
        learner_id=learner_id,
    )
    recommendations = generate_recommendations(
        db=db,
        learner_id=learner_id,
    )

    skill_scores = performance.average_scores_by_skill
    average_score = (
        sum(
            skill.average_score
            for skill in skill_scores
        )
        / len(skill_scores)
        if skill_scores
        else None
    )

    weakest_skill = (
        skill_scores[0].skill
        if skill_scores
        else None
    )

    strongest_skill = (
        strengths.highest_performing_skills[0].skill
        if strengths.highest_performing_skills
        else (
            skill_scores[-1].skill
            if skill_scores
            else None
        )
    )

    todays_recommendation = (
        recommendations.recommendations[0]
        if recommendations.recommendations
        else None
    )

    if todays_recommendation:
        ai_insight = (
            f"Focus on {todays_recommendation.affected_skill.replace('_', ' ')} "
            f"because {todays_recommendation.reason}"
        )
    elif performance.practice_frequency.total_practices == 0:
        ai_insight = (
            "No evaluated practice history is available yet."
        )
    else:
        ai_insight = (
            "Current learner data does not show a high-priority "
            "weakness. Continue balanced practice."
        )

    return DashboardInsights(
        learner_id=learner_id,
        current_level=_current_level(average_score),
        current_focus=(
            todays_recommendation.affected_skill
            if todays_recommendation
            else weakest_skill
        ),
        todays_recommendation=todays_recommendation,
        strongest_skill=strongest_skill,
        weakest_skill=weakest_skill,
        practice_streak=(
            performance.practice_frequency.current_streak
        ),
        weekly_improvement=performance.improvement_rate,
        ai_insight=ai_insight,
    )


def get_learner_intelligence(
    db: Session,
    learner_id: int,
) -> LearnerIntelligenceResponse:
    performance = analyze_performance(
        db=db,
        learner_id=learner_id,
    )
    weaknesses = detect_weaknesses(
        db=db,
        learner_id=learner_id,
    )
    strengths = detect_strengths(
        db=db,
        learner_id=learner_id,
    )
    recommendations = generate_recommendations(
        db=db,
        learner_id=learner_id,
    )
    learning_path = generate_learning_path(
        db=db,
        learner_id=learner_id,
    )
    dashboard_insights = generate_dashboard_insights(
        db=db,
        learner_id=learner_id,
    )

    return LearnerIntelligenceResponse(
        performance=performance,
        weaknesses=weaknesses,
        strengths=strengths,
        recommendations=recommendations,
        learning_path=learning_path,
        dashboard_insights=dashboard_insights,
    )
