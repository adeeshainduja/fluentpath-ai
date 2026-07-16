import api from "../api/axios";
import type {
  DashboardInsights,
  LearnerIntelligenceResponse,
  LearnerRecommendations,
} from "../types/learnerIntelligence";

export const getLearnerIntelligence = async (
  learnerId: number
): Promise<LearnerIntelligenceResponse> => {
  const response = await api.get(
    `/learner-intelligence/learners/${learnerId}`
  );

  return response.data;
};

export const getLearnerRecommendations = async (
  learnerId: number
): Promise<LearnerRecommendations> => {
  const response = await api.get(
    `/learner-intelligence/learners/${learnerId}/recommendations`
  );

  return response.data;
};

export const getDashboardInsights = async (
  learnerId: number
): Promise<DashboardInsights> => {
  const response = await api.get(
    `/learner-intelligence/learners/${learnerId}/dashboard-insights`
  );

  return response.data;
};
