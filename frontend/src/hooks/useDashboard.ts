import { useQuery } from "@tanstack/react-query";
import { getDashboard } from "../api/dashboard";

export const useDashboard = (learnerId: number) => {
  return useQuery({
    queryKey: ["dashboard", learnerId],
    queryFn: () => getDashboard(learnerId),
  });
};