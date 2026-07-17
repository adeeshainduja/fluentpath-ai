import api from "../api/axios";
import type {
  ReadingPractice,
  ReadingSubmissionRequest,
  ReadingSubmissionResponse,
} from "../types/reading";

export const generateReadingPractice = async (): Promise<ReadingPractice> => {
  const response = await api.get<ReadingPractice>(
    "/reading/generate"
  );

  return response.data;
};

export const submitReadingPractice = async (
  payload: ReadingSubmissionRequest
): Promise<ReadingSubmissionResponse> => {
  const response = await api.post<ReadingSubmissionResponse>(
    "/reading/submit",
    payload
  );

  return response.data;
};
