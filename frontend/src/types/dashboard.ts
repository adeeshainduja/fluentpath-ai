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
  total_attempts: number;
  average_score: number;
  first_score: number;
  latest_score: number;
  score_change: number;
  trend: string;
}

export interface TimelineItem {
  date: string;
  practice_count: number;
  average_score: number;
}

export interface PracticeHistoryItem {
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

export interface Recommendation {
  strategy: string | null;
  priority_skill?: string | null;
  selected_skill?: string | null;
  reason: string | null;
}

export interface WeakSkill {
  skill: string;
  score: number;
  priority: string;
  recommendation: string;
}

export interface ErrorStatistics {
  total_errors: number;
  active_errors?: number;
  resolved_errors?: number;
  error_distribution: Record<string, unknown>;
}

export interface TrendAnalytics {
  trend: string;
  average_score: number;
  recent_average: number;
  highest_score?: number;
  lowest_score?: number;
  total_attempts?: number;
}

export interface DailyMission {
  skill: string;
  target: number;
  completed: number;
  priority: number;
}

export interface AchievementBadge {
  title: string;
  description: string;
  earned: boolean;
  icon: string;
}

export interface DashboardResponse {
  summary: DashboardSummary;

  skill_progress: SkillProgress[];

  learning_timeline: TimelineItem[];

  practice_history: PracticeHistoryItem[];

  recommendations: Recommendation;

  error_statistics: ErrorStatistics;

  trend_analytics: TrendAnalytics;

  weak_skills: WeakSkill[];

  daily_missions: DailyMission[];

  achievement_badges: AchievementBadge[];
}
