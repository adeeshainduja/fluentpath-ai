import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { sendAICoachMessage } from "../services/aiCoachApi";
import type {
  AICoachChatRequest,
  AICoachResponse,
} from "../types/aiCoach";

export function useAICoach() {
  return useQuery<AICoachResponse>({
    queryKey: ["ai-coach"],
    queryFn: async () => {
      const response = await sendAICoachMessage({
        message: "What should I practice today?",
      });

      return response;
    },
    staleTime: 1000 * 30,
  });
}

export function useSendAICoachMessage() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: AICoachChatRequest) =>
      sendAICoachMessage(payload),
    onSuccess: (data) => {
      queryClient.setQueryData(["ai-coach"], data);
    },
  });
}
