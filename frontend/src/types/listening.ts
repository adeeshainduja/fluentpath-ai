export interface ListeningQuestion {
  id: number;
  question: string;
  options: string[];
}

export interface ListeningPractice {
  practice_id: string;
  audio_url: string;
  transcript: string;
  estimated_minutes: number;
  questions: ListeningQuestion[];
}

export interface ListeningSubmissionRequest {
  learner_id?: number;
  practice_id: string;
  answers: Record<number, string>;
}

export interface ListeningSubmissionResponse {
  attempt_id: number;
  score: number;
  correct_answers: Record<number, string>;
  explanations: Record<number, string>;
  feedback: string;
  ai_feedback: string;
  user_answers: Record<number, string>;
  transcript: string;
  audio_url: string;
}
