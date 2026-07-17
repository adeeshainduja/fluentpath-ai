export interface ReadingQuestion {
  id: number;
  question: string;
  options: string[];
}

export interface ReadingPassage {
  title: string;
  text: string;
}

export interface ReadingPractice {
  passage_id: string;
  passage: ReadingPassage;
  estimated_minutes: number;
  questions: ReadingQuestion[];
}

export interface ReadingSubmissionRequest {
  learner_id?: number;
  passage_id: string;
  answers: Record<number, string>;
}

export interface ReadingSubmissionResponse {
  attempt_id: number;
  score: number;
  correct_answers: Record<number, string>;
  explanations: Record<number, string>;
  feedback: string;
  user_answers: Record<number, string>;
}
