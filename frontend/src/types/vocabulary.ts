export interface VocabularyQuestion {
  id: number;
  word: string;
  question: string;
  options: string[];
}

export interface VocabularyPractice {
  sessionId: number;
  difficulty: string;
  questions: VocabularyQuestion[];
}

export interface VocabularyAnswer {
  questionId: number;
  selectedOption: string;
}

export interface VocabularySubmissionRequest {
  sessionId: number;
  answers: VocabularyAnswer[];
}

export interface VocabularySubmissionResponse {
  score: number;
  correctAnswers: Record<number, string>;
  explanations: Record<number, string>;
  feedback: string;
}
