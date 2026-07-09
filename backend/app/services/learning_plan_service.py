from sqlalchemy.orm import Session

from app.agents.learning_plan_agent import (
    create_learning_plan,
)
from app.memory.learner_memory import (
    get_learner_weaknesses,
)


def generate_learning_plan(
    db: Session,
    learner_id: int,
):

    weaknesses = get_learner_weaknesses(
        db=db,
        learner_id=learner_id,
    )

    plan = create_learning_plan(
        learner_id=learner_id,
        weaknesses=weaknesses,
    )

    return plan