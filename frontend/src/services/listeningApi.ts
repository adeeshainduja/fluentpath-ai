import api from "../api/axios";
import type {
  ListeningPractice,
  ListeningSubmissionRequest,
  ListeningSubmissionResponse,
} from "../types/listening";

export const generateListeningPractice =
  async (): Promise<ListeningPractice> => {
    const response = await api.get<ListeningPractice>(
      "/listening/generate"
    );

    return response.data;
  };

export const submitListeningPractice = async (
  payload: ListeningSubmissionRequest
): Promise<ListeningSubmissionResponse> => {
  const response =
    await api.post<ListeningSubmissionResponse>(
      "/listening/submit",
      payload
    );

  return response.data;
};
