export interface AnalyticsPeriodPoint {
  period: string;
  average_score: number;
  practice_count: number;
}

export interface AnalyticsDatePoint {
  date: string;
  score: number;
}

export interface AnalyticsChartPoint {
  label: string;
  value: number;
}

export interface AnalyticsSkillTrend {
  skill: string;
  total_attempts: number;
  average_score: number;
  first_score: number;
  latest_score: number;
  score_change: number;
  trend: string;
}

export interface AnalyticsPracticeDistribution {
  practice_type: string;
  count: number;
  percentage: number;
}

export interface AnalyticsResponse {
  overall_performance: number;
  average_score: number;
  total_practices: number;
  practice_minutes: number;
  weekly_progress: number;
  monthly_progress: number;
  reading_accuracy: number;
  listening_accuracy: number;
  speaking_accuracy: number;
  writing_accuracy: number;
  vocabulary_accuracy: number;
  daily_streak: number;
  weakest_skill: string;
  strongest_skill: string;
  practice_distribution: AnalyticsPracticeDistribution[];
  recent_improvement: number;
  skill_trend: AnalyticsSkillTrend[];
  weekly_score_trend: AnalyticsPeriodPoint[];
  monthly_score_trend: AnalyticsPeriodPoint[];
  practice_type_distribution: AnalyticsPracticeDistribution[];
  skill_comparison: AnalyticsChartPoint[];
  progress_timeline: AnalyticsDatePoint[];
  daily_activity: AnalyticsDatePoint[];
  recent_attempts: Array<Record<string, unknown>>;
  insights: string[];
  summary?: Record<string, unknown> | null;
}
