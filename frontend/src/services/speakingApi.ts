import api from "../api/axios";
import type { SpeakingResponse } from "../types/speaking";

export async function evaluateSpeaking(
  transcript: string,
  learnerId?: number
): Promise<SpeakingResponse> {
  const response = await api.post<SpeakingResponse>(
    "/speaking/evaluate",
    {
      transcript,
      learner_id: learnerId,
    }
  );

  return response.data;
}
