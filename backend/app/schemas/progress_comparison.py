from pydantic import BaseModel


class ProgressComparisonResult(BaseModel):
    improved: bool

    previous_score: int
    current_score: int
    score_change: int

    relevance_improved: bool
    detail_improved: bool
    target_skill_improved: bool

    movement_summary: str
    positive_change: str
    remaining_focus: str
    next_action: str