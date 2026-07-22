import api from "./axios";
import type {
  LearningPathResponse,
  LearningPathUpdateResponse,
} from "../types/learningPath";

export const getLearningPath = async (): Promise<LearningPathResponse> => {
  const response = await api.get<LearningPathResponse>("/learning-path");
  return response.data;
};

export const updateLearningPath = async (): Promise<LearningPathUpdateResponse> => {
  const response = await api.post<LearningPathUpdateResponse>("/learning-path/update");
  return response.data;
};
