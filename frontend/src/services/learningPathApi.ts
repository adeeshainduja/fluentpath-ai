import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api/v1";

export interface RoadmapItem {
  id: number;
  title: string;
  skill: string;
 difficulty: string;
  estimated_minutes: number;
  status: "completed" | "current" | "locked";
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

export const getLearningPath = async (
  learnerId: number
): Promise<LearningPathResponse> => {
  const response = await axios.get(
    `${API_BASE_URL}/learning-path/${learnerId}`
  );

  return response.data;
};