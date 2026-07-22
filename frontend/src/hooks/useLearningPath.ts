import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { getLearningPath, updateLearningPath } from "../services/learningPathApi";

export function useLearningPath() {
  return useQuery({
    queryKey: ["learning-path"],
    queryFn: getLearningPath,
    staleTime: 1000 * 60,
  });
}

export function useRefreshLearningPath() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateLearningPath,
    onSuccess: (data) => {
      queryClient.setQueryData(["learning-path"], data.path);
      queryClient.invalidateQueries({ queryKey: ["learning-path"] });
    },
  });
}
