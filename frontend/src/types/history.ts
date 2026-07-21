export type PracticeType =
  | "all"
  | "reading"
  | "listening"
  | "writing"
  | "speaking"
  | "vocabulary";

export interface PracticeHistoryItem {
  attempt_id: number;
  practice_type: string;
  title: string;
  completed_date: string;
  score?: number | null;
  duration?: number | null;
  difficulty?: string | null;
  feedback_summary?: string | null;
  status: string;
  target_skill?: string | null;
}

export interface PracticeHistoryResponse {
  total: number;
  page: number;
  limit: number;
  items: PracticeHistoryItem[];
}

export interface PracticeHistoryDetail {
  attempt_id: number;
  practice_type: string;
  title: string;
  completed_date: string;
  score?: number | null;
  duration?: number | null;
  difficulty?: string | null;
  status: string;
  original_practice: Record<string, unknown>;
  learner_answers: Record<string, unknown>;
  correct_answers?: Record<string, unknown> | null;
  explanations?: Record<string, unknown> | null;
  ai_feedback?: string | null;
  feedback_summary?: string | null;
  weaknesses: string[];
  strengths: string[];
  completion_time?: string | null;
  suggestions: string[];
}

export interface PracticeHistoryDetailResponse {
  history: PracticeHistoryDetail;
}
