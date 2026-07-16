export interface HistoryItem {
  record_id: string;
  source: "practice_attempt" | "speaking_attempt";
  attempt_id: number;
  learner_id: number;
  practice_type: string;
  task_id?: number | null;
  task_title?: string | null;
  target_skill?: string | null;
  submitted_text: string;
  score?: number | null;
  grammar_score?: number | null;
  vocabulary_score?: number | null;
  fluency_score?: number | null;
  pronunciation_score?: number | null;
  confidence_score?: number | null;
  feedback?: string | null;
  has_evaluation: boolean;
  created_at: string;
}

export interface HistoryResponse {
  learner_id: number;
  total: number;
  limit: number;
  offset: number;
  items: HistoryItem[];
}
