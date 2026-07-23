import api from "../api/axios";;
import type { AdaptivePracticeRecommendation } from "../types/adaptivePractice";

export async function getRecommendation(): Promise<AdaptivePracticeRecommendation> {
  const response = await api.get<AdaptivePracticeRecommendation>(
    "/practice/recommend"
  );

  return response.data;
}
