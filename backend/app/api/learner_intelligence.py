from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.learner_intelligence import (
    AdaptiveLearningPath,
    DashboardInsights,
    LearnerIntelligenceResponse,
    LearnerPerformanceAnalysis,
    LearnerRecommendations,
    LearnerStrengths,
    LearnerWeaknesses,
)
from app.services.learner_intelligence_service import (
    analyze_performance,
    detect_strengths,
    detect_weaknesses,
    generate_dashboard_insights,
    generate_learning_path,
    generate_recommendations,
    get_learner_intelligence,
)


router = APIRouter(
    prefix="/api/v1/learner-intelligence",
    tags=["Learner Intelligence"],
)


@router.get(
    "/learners/{learner_id}",
    response_model=LearnerIntelligenceResponse,
)
def learner_intelligence(
    learner_id: int,
    db: Session = Depends(get_db),
):
    return get_learner_intelligence(
        db=db,
        learner_id=learner_id,
    )


@router.get(
    "/learners/{learner_id}/performance",
    response_model=LearnerPerformanceAnalysis,
)
def learner_performance(
    learner_id: int,
    db: Session = Depends(get_db),
):
    return analyze_performance(
        db=db,
        learner_id=learner_id,
    )


@router.get(
    "/learners/{learner_id}/weaknesses",
    response_model=LearnerWeaknesses,
)
def learner_weaknesses(
    learner_id: int,
    db: Session = Depends(get_db),
):
    return detect_weaknesses(
        db=db,
        learner_id=learner_id,
    )


@router.get(
    "/learners/{learner_id}/strengths",
    response_model=LearnerStrengths,
)
def learner_strengths(
    learner_id: int,
    db: Session = Depends(get_db),
):
    return detect_strengths(
        db=db,
        learner_id=learner_id,
    )


@router.get(
    "/learners/{learner_id}/recommendations",
    response_model=LearnerRecommendations,
)
def learner_recommendations(
    learner_id: int,
    db: Session = Depends(get_db),
):
    return generate_recommendations(
        db=db,
        learner_id=learner_id,
    )


@router.get(
    "/learners/{learner_id}/learning-path",
    response_model=AdaptiveLearningPath,
)
def learner_learning_path(
    learner_id: int,
    db: Session = Depends(get_db),
):
    return generate_learning_path(
        db=db,
        learner_id=learner_id,
    )


@router.get(
    "/learners/{learner_id}/dashboard-insights",
    response_model=DashboardInsights,
)
def learner_dashboard_insights(
    learner_id: int,
    db: Session = Depends(get_db),
):
    return generate_dashboard_insights(
        db=db,
        learner_id=learner_id,
    )
