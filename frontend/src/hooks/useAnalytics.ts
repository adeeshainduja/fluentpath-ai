import { useQuery } from "@tanstack/react-query";
import { getAnalytics } from "../services/analyticsApi";

export const useAnalytics = () => {
  return useQuery({
    queryKey: ["analytics"],
    queryFn: getAnalytics,
  });
};
