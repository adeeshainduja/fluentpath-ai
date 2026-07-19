import api from "../api/axios";
import type {
  VocabularyPractice,
  VocabularySubmissionRequest,
  VocabularySubmissionResponse,
} from "../types/vocabulary";

export const generateVocabularyPractice =
  async (): Promise<VocabularyPractice> => {
    const response = await api.get<VocabularyPractice>(
      "/vocabulary/generate"
    );

    return response.data;
  };

export const submitVocabularyPractice = async (
  payload: VocabularySubmissionRequest
): Promise<VocabularySubmissionResponse> => {
  const response = await api.post<VocabularySubmissionResponse>(
    "/vocabulary/submit",
    payload
  );

  return response.data;
};
