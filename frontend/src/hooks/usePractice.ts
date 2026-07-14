import { useEffect, useState } from "react";
import { getPractice } from "../api/practice";

export function usePractice(id: number) {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<any>(null);

  useEffect(() => {
    async function load() {
      try {
        const result = await getPractice(id);
        setData(result);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [id]);

  return {
    data,
    loading,
    error,
  };
}