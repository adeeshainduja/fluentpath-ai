import api from "./axios";
import type { DashboardResponse } from "../types/dashboard";

export const getDashboard = async (
  learnerId?: number
): Promise<DashboardResponse> => {
  const response = await api.get(
    learnerId ? `/dashboard/${learnerId}` : "/dashboard"
  );
  return response.data;
};
