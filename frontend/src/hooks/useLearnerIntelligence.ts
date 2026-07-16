import { useQuery } from "@tanstack/react-query";
import { getLearnerIntelligence } from "../services/learnerIntelligenceApi";

export const useLearnerIntelligence = (
  learnerId: number
) => {
  return useQuery({
    queryKey: [
      "learner-intelligence",
      learnerId,
    ],
    queryFn: () =>
      getLearnerIntelligence(learnerId),
    staleTime: 1000 * 60 * 5,
  });
};
