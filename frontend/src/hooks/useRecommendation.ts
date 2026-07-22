import { useQuery } from "@tanstack/react-query";
import { getRecommendation } from "../services/recommendationApi";

export function useRecommendation() {
  return useQuery({
    queryKey: ["adaptive-practice-recommendation"],
    queryFn: getRecommendation,
  });
}
