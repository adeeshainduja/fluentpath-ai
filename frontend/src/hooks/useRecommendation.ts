import { useEffect, useState } from "react";

import { getRecommendation } from "../services/recommendationApi";

export function useRecommendation(
  learnerId: number
) {
  const [data, setData] = useState<any>(null);

  const [isLoading, setLoading] =
    useState(true);

  const [error, setError] =
    useState(false);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);

        const result =
          await getRecommendation(learnerId);

        setData(result);
      } catch {
        setError(true);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [learnerId]);

  return {
    data,
    isLoading,
    error,
  };
}