from sqlalchemy.orm import Session


def get_achievement_badges(db: Session, learner_id: int):
    return [
        {
            "title": "Grammar Master",
            "description": "Score above 80 in Grammar",
            "earned": True,
            "icon": "award",
        },
        {
            "title": "7 Day Streak",
            "description": "Practice for 7 consecutive days",
            "earned": False,
            "icon": "flame",
        },
        {
            "title": "Vocabulary Pro",
            "description": "Complete 20 vocabulary exercises",
            "earned": True,
            "icon": "book",
        },
    ]