export interface AICoachChatMessage {
  role: "user" | "assistant";
  message: string;
  summary?: string | null;
  current_focus?: string | null;
  previous_recommendation?: string | null;
  created_at: string;
}

export interface AICoachLearnerSummary {
  current_level: string;
  overall_progress: number;
  current_focus: string;
  recommended_practice: string;
  weak_skills: string[];
  strong_skills: string[];
  recent_practices: Array<Record<string, unknown>>;
  average_score: number;
}

export interface AICoachNextAction {
  title: string;
  description: string;
}

export interface AICoachResponse {
  reply: string;
  conversation_history: AICoachChatMessage[];
  suggested_questions: string[];
  current_learner_summary: AICoachLearnerSummary;
  recommended_next_action: AICoachNextAction;
  weak_skills: string[];
  strong_skills: string[];
  current_learning_path: {
    current_level: string;
    overall_progress: number;
    current_focus: string;
    recommended_practice: string;
    next_milestone: string;
    tasks: Array<{ title: string; completed: boolean }>;
    weak_skills: string[];
    strong_skills: string[];
    learning_timeline: Array<{ date: string; score: number }>;
    skill_roadmap: Array<{
      skill: string;
      priority: string;
      target_score: number;
    }>;
    weekly_tasks: Array<{ title: string; completed: boolean }>;
    completed_tasks: Array<{ title: string; completed: boolean }>;
    progress_bar: number;
    today_recommendation: string;
  };
}

export interface AICoachChatRequest {
  message: string;
}
