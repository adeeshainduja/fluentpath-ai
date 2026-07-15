import { useQuery } from "@tanstack/react-query";
import axios from "axios";

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

const fetchLearningPath = async (
  learnerId: number
): Promise<LearningPathResponse> => {
  const { data } = await axios.get(
    `http://localhost:8000/api/v1/learning-path/${learnerId}`
  );

  return data;
};

export function useLearningPath(
  learnerId: number
) {
  return useQuery({
    queryKey: ["learning-path", learnerId],

    queryFn: () =>
      fetchLearningPath(learnerId),

    staleTime: 1000 * 60 * 5,
  });
}