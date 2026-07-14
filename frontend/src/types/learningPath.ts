export type LessonStatus =
  | "completed"
  | "current"
  | "locked";

export interface RoadmapItem {
  id: number;
  title: string;
  skill: string;
  difficulty: string;
  estimated_minutes: number;
  status: LessonStatus;
}

export interface CurrentStage {
  id: number;
  title: string;
  skill: string;
  difficulty: string;
  estimated_minutes: number;
}

export interface Badge {
  id: number;
  title: string;
  description: string;
  earned: boolean;
}

export interface LearningPathResponse {
  overall_progress: number;

  streak: number;

  coach_message: string;

  current_stage: CurrentStage;

  roadmap: RoadmapItem[];

  badges: Badge[];
}