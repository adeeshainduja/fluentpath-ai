export interface DashboardSummary {
  average_score: number;
  completed_tasks: number;
  pending_tasks: number;
  learning_trend: string;
  recommended_skill: string | null;
  recommended_strategy: string | null;
}

export interface SkillProgress {
  skill: string;
  average_score: number;
  trend: string;
}

export interface TimelineItem {
  date: string;
  practice_count: number;
  average_score: number;
}

export interface PracticeHistory {
  task_id: number;
  task_type: string;
  difficulty: string;
  status: string;
  created_at: string;
}

export interface ErrorStatistics {
  total_errors: number;
  error_distribution: Record<string, number>;
}

export interface TrendAnalytics {
  trend: string;
  average_score: number;
  recent_average: number;
}

export interface Recommendation {
  strategy: string;
  selected_skill: string;
  reason: string;
}

export interface DashboardResponse {
  summary: DashboardSummary;
  skill_progress: SkillProgress[];
  learning_timeline: TimelineItem[];
  practice_history: PracticeHistory[];
  recommendations: Recommendation;
  error_statistics: ErrorStatistics;
  trend_analytics: TrendAnalytics;
}