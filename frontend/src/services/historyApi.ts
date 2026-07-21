import api from "../api/axios";
import type {
  PracticeHistoryDetailResponse,
  PracticeHistoryResponse,
  PracticeType,
} from "../types/history";

export interface PracticeHistoryQuery {
  page?: number;
  limit?: number;
  type?: PracticeType;
  sort?: "newest" | "oldest" | "score_desc" | "score_asc";
  search?: string;
}

export async function getHistory(
  query: PracticeHistoryQuery = {}
): Promise<PracticeHistoryResponse> {
  const response = await api.get<PracticeHistoryResponse>(
    "/practice-history",
    { params: query }
  );

  return response.data;
}

export async function getHistoryDetail(
  attemptId: number
): Promise<PracticeHistoryDetailResponse> {
  const response = await api.get<PracticeHistoryDetailResponse>(
    `/practice-history/${attemptId}`
  );

  return response.data;
}
