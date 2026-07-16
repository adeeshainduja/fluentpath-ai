import api from "../api/axios";
import type { HistoryResponse } from "../types/history";

export async function getHistory(): Promise<HistoryResponse> {
  const response = await api.get<HistoryResponse>(
    "/history"
  );

  return response.data;
}
