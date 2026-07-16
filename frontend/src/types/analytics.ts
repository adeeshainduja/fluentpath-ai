export interface PeriodProgress {
  period: string;
  average_score: number;
  practice_count: number;
}

export interface SkillImprovement {
  skill: string;
  average_score: number;
  latest_score: number;
  score_change: number;
  trend: string;
}

export interface GrammarMistake {
  category: string;
  error_type: string;
  occurrences: number;
  resolved: number;
  active: number;
}

export interface ScorePoint {
  date: string;
  score: number;
}

export interface AnalyticsResponse {
  weekly_progress: PeriodProgress[];
  monthly_progress: PeriodProgress[];
  skill_improvements: SkillImprovement[];
  grammar_mistakes: GrammarMistake[];
  vocabulary_growth: ScorePoint[];
  pronunciation_trend: ScorePoint[];
  summary: {
    average_score: number;
    weekly_change: number;
    vocabulary_growth: number;
    pronunciation_trend: number;
  };
}
