from collections import defaultdict


def get_skill_progress(
    db: Session,
    learner_id: int,
):
    metrics = (
        db.query(ProgressMetric)
        .filter(
            ProgressMetric.learner_id == learner_id
        )
        .order_by(
            ProgressMetric.created_at.asc()
        )
        .all()
    )

    skill_groups = defaultdict(list)

    for metric in metrics:
        skill_groups[metric.target_skill].append(metric)

    skill_progress = []

    for skill, skill_metrics in skill_groups.items():
        scores = [
            metric.task_score
            for metric in skill_metrics
        ]

        average_score = round(
            sum(scores) / len(scores),
            2,
        )

        first_score = scores[0]
        latest_score = scores[-1]

        score_change = latest_score - first_score

        if score_change >= 10:
            trend = "improving"

        elif score_change <= -10:
            trend = "declining"

        else:
            trend = "stable"

        skill_progress.append(
            {
                "skill": skill,
                "total_attempts": len(skill_metrics),
                "average_score": average_score,
                "first_score": first_score,
                "latest_score": latest_score,
                "score_change": score_change,
                "trend": trend,
            }
        )

    return skill_progress

def get_skill_priorities(
    db: Session,
    learner_id: int,
):
    skills = get_skill_progress(
        db=db,
        learner_id=learner_id,
    )

    priorities = []

    for skill in skills:
        weakness_score = 100 - skill["average_score"]

        if skill["trend"] == "declining":
            weakness_score += 15

        elif skill["trend"] == "improving":
            weakness_score -= 5

        weakness_score = max(
            0,
            min(100, weakness_score),
        )

        priorities.append(
            {
                "skill": skill["skill"],
                "priority_score": round(
                    weakness_score,
                    2,
                ),
                "average_score": skill["average_score"],
                "trend": skill["trend"],
            }
        )

    priorities.sort(
        key=lambda item: item["priority_score"],
        reverse=True,
    )

    return priorities