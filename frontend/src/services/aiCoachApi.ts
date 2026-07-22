import api from "../api/axios";
import type {
  AICoachChatRequest,
  AICoachResponse,
} from "../types/aiCoach";

export const sendAICoachMessage = async (
  payload: AICoachChatRequest
): Promise<AICoachResponse> => {
  const response = await api.post<AICoachResponse>(
    "/ai-coach/chat",
    payload
  );

  return response.data;
};
