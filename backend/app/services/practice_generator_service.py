from sqlalchemy.orm import Session

from app.models.practice_task import PracticeTask

from app.services.learning_plan_service import (
    generate_learning_plan,
)


def generate_practice_task(
    db: Session,
    learner_id: int,
    practice_type: str,
) -> PracticeTask:
    """
    Generate a personalized practice task
    based on the selected practice type.
    """

    recommendation = generate_learning_plan(
        db=db,
        learner_id=learner_id,
    )

    target_skill = recommendation["target_skill"]
    difficulty = recommendation["difficulty"]

    title = ""
    instruction = ""

    # ----------------------------------------
    # Writing
    # ----------------------------------------

    if practice_type == "writing":

        title = f"{target_skill} Writing Exercise"

        instruction = (
            f"Write 150-200 words focusing on "
            f"{target_skill.lower()}."
        )

    # ----------------------------------------
    # Speaking
    # ----------------------------------------

    elif practice_type == "speaking":

        title = f"{target_skill} Speaking Practice"

        instruction = (
            "Speak for two minutes about the given topic."
        )

    # ----------------------------------------
    # Reading
    # ----------------------------------------

    elif practice_type == "reading":

        title = f"{target_skill} Reading Practice"

        instruction = (
            "Read the passage carefully and answer the questions."
        )

    # ----------------------------------------
    # Listening
    # ----------------------------------------

    elif practice_type == "listening":

        title = f"{target_skill} Listening Practice"

        instruction = (
            "Listen to the audio and summarize the content."
        )

    # ----------------------------------------
    # Vocabulary
    # ----------------------------------------

    elif practice_type == "vocabulary":

        title = f"{target_skill} Vocabulary Builder"

        instruction = (
            "Complete the vocabulary challenge."
        )

    # ----------------------------------------
    # Interview
    # ----------------------------------------

    elif practice_type == "interview":

        title = "Mock Interview"

        instruction = (
            "Answer the interview question naturally."
        )

    else:

        raise ValueError(
            f"Unsupported practice type: {practice_type}"
        )

    task = PracticeTask(
        learner_id=learner_id,
        target_skill=target_skill,
        practice_type=practice_type,
        difficulty=difficulty,
        title=title,
        instruction=instruction,
        strategy=recommendation.get("strategy"),
        status="pending",
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task