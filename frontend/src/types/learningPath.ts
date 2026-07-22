export interface LearningPathTask {
  title: string;
  completed: boolean;
}

export interface LearningPathResponse {
  current_level: string;
  overall_progress: number;
  current_focus: string;
  recommended_practice: string;
  next_milestone: string;
  tasks: LearningPathTask[];
  weak_skills: string[];
  strong_skills: string[];
  learning_timeline: Array<{ date: string; score: number }>;
  skill_roadmap: Array<{
    skill: string;
    priority: string;
    target_score: number;
  }>;
  weekly_tasks: LearningPathTask[];
  completed_tasks: LearningPathTask[];
  progress_bar: number;
  today_recommendation: string;
}

export interface LearningPathUpdateResponse {
  status: "updated";
  path: LearningPathResponse;
}
