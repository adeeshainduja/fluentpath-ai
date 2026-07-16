import api from "../api/axios";
import type { AnalyticsResponse } from "../types/analytics";

export async function getAnalytics(): Promise<AnalyticsResponse> {
  const response = await api.get<AnalyticsResponse>(
    "/analytics"
  );

  return response.data;
}
