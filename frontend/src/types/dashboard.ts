export interface DashboardWeeklyProgress {
  completed: number;
  target: number;
  percentage: number;
}

export interface LegacyDashboardSummary {
  average_score: number;
  daily_streak: number;
  total_practices: number;
  completed_tasks: number;
  pending_tasks: number;
  learning_trend: string;
  recommended_skill: string | null;
  recommended_strategy: string | null;
}

export interface LegacySkillProgress {
  skill: string;
  total_attempts: number;
  average_score: number;
  first_score: number;
  latest_score: number;
  score_change: number;
  trend: string;
}

export interface LegacyTimelineItem {
  date: string;
  practice_count: number;
  average_score: number;
}

export interface LegacyPracticeHistoryItem {
  task_id: number;
  title?: string;
  target_skill: string;
  practice_type?: string;
  difficulty?: string;
  status?: string;
  strategy?: string;
  task_score?: number;
  created_at: string;
}

export interface LegacyRecommendation {
  strategy: string | null;
  priority_skill?: string | null;
  selected_skill?: string | null;
  reason: string | null;
}

export interface LegacyErrorStatistics {
  total_errors: number;
  active_errors?: number;
  resolved_errors?: number;
  error_distribution: Record<string, unknown>;
}

export interface LegacyTrendAnalytics {
  trend: string;
  average_score: number;
  recent_average: number;
  highest_score?: number;
  lowest_score?: number;
  total_attempts?: number;
}

export interface DashboardAchievement {
  title: string;
  description: string | null;
  earned: boolean;
  icon: string;
}

export interface DashboardPracticeItem {
  task_id: number | null;
  title: string | null;
  practice_type: string | null;
  target_skill: string | null;
  score: number | null;
  created_at: string;
}

export interface DashboardResponse {
  learner_name: string;
  total_practices: number;
  average_score: number;
  reading_score: number;
  listening_score: number;
  speaking_score: number;
  writing_score: number;
  vocabulary_score: number;
  daily_streak: number;
  weekly_goal_progress: DashboardWeeklyProgress;
  completed_practices_this_week: number;
  achievements: DashboardAchievement[];
  latest_practice: DashboardPracticeItem | null;
  ai_recommendation_summary: string | null;
  summary: LegacyDashboardSummary;
  skill_progress: LegacySkillProgress[];
  learning_timeline: LegacyTimelineItem[];
  practice_history: LegacyPracticeHistoryItem[];
  recommendations: LegacyRecommendation;
  error_statistics: LegacyErrorStatistics;
  trend_analytics: LegacyTrendAnalytics;
  weak_skills: WeakSkill[];
  daily_missions: DailyMission[];
  achievement_badges: DashboardAchievement[];
}

export interface DailyMission {
  skill: string;
  target: number;
  completed: number;
  priority: number;
}

export interface WeakSkill {
  skill: string;
  score: number;
  priority: string;
  recommendation: string;
}
