export interface SkillAverage {
  skill: string;
  average_score: number;
  attempts: number;
  latest_score: number | null;
  trend: string;
}

export interface ScoreTrendPoint {
  date: string;
  score: number;
  practice_type: string;
  skill: string | null;
}

export interface PracticeFrequency {
  total_practices: number;
  active_days: number;
  practices_last_7_days: number;
  practices_last_30_days: number;
  average_practices_per_active_day: number;
  current_streak: number;
}

export interface LearnerPerformanceAnalysis {
  learner_id: number;
  average_scores_by_skill: SkillAverage[];
  speaking_trend: ScoreTrendPoint[];
  writing_trend: ScoreTrendPoint[];
  practice_frequency: PracticeFrequency;
  improvement_rate: number | null;
  consistency: number | null;
  consistency_label: string;
}

export interface WeaknessInsight {
  skill: string;
  category: string;
  score: number | null;
  evidence: string;
  severity: string;
  priority: number;
}

export interface LearnerWeaknesses {
  learner_id: number;
  grammar_topics: WeaknessInsight[];
  vocabulary_weaknesses: WeaknessInsight[];
  pronunciation_weaknesses: WeaknessInsight[];
  fluency_weaknesses: WeaknessInsight[];
  confidence_weaknesses: WeaknessInsight[];
}

export interface StrengthInsight {
  skill: string;
  category: string;
  score: number;
  evidence: string;
  consistency: number | null;
}

export interface LearnerStrengths {
  learner_id: number;
  highest_performing_skills: StrengthInsight[];
  most_improved_skills: StrengthInsight[];
  consistent_strengths: StrengthInsight[];
}

export interface LearnerRecommendation {
  recommendation: string;
  reason: string;
  affected_skill: string;
  confidence: number;
  priority: number;
  suggested_practice_type: string;
}

export interface LearnerRecommendations {
  learner_id: number;
  recommendations: LearnerRecommendation[];
}

export interface LearningGoal {
  goal: string;
  target_skill: string;
  reason: string;
  suggested_practice_type: string;
  priority: number;
  success_metric: string;
}

export interface AdaptiveLearningPath {
  learner_id: number;
  current_level: string;
  progress: number | null;
  current_focus: string | null;
  current_goal: string | null;
  recommended_practice: LearnerRecommendation | null;
  completed_skills: string[];
  remaining_skills: string[];
  goals: LearningGoal[];
}

export interface DashboardInsights {
  learner_id: number;
  current_level: string;
  current_focus: string | null;
  todays_recommendation: LearnerRecommendation | null;
  strongest_skill: string | null;
  weakest_skill: string | null;
  practice_streak: number;
  weekly_improvement: number | null;
  ai_insight: string;
}

export interface LearnerIntelligenceResponse {
  performance: LearnerPerformanceAnalysis;
  weaknesses: LearnerWeaknesses;
  strengths: LearnerStrengths;
  recommendations: LearnerRecommendations;
  learning_path: AdaptiveLearningPath;
  dashboard_insights: DashboardInsights;
}
