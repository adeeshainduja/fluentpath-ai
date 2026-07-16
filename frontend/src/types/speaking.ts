export interface SpeakingEvaluation {
  grammar_score: number;
  vocabulary_score: number;
  fluency_score: number;
  pronunciation_score: number;
  confidence_score: number;
  grammar_feedback: string;
  vocabulary_feedback: string;
  pronunciation_feedback: string;
  fluency_feedback: string;
  overall_feedback: string;
  suggestions: string[];
}

export interface SpeakingResponse {
  attempt_id: number;
  transcript: string;
  score: number;
  pronunciation: {
    score: number;
    fluency: number;
    confidence: number;
    pronunciation: number;
    comments: string[];
  };
  evaluation: SpeakingEvaluation;
  coach_message: string;
}
