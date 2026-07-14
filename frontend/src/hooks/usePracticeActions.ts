import { useState } from "react";
import {
  submitPractice,
  regeneratePractice,
  completePractice,
} from "../api/practice";

export function usePracticeActions() {
  const [loading, setLoading] = useState(false);

  const submit = async (
    id: number,
    answer: string
  ) => {
    setLoading(true);

    try {
      return await submitPractice(id, answer);
    } finally {
      setLoading(false);
    }
  };

  const regenerate = async (id: number) => {
    setLoading(true);

    try {
      return await regeneratePractice(id);
    } finally {
      setLoading(false);
    }
  };

  const complete = async (id: number) => {
    setLoading(true);

    try {
      return await completePractice(id);
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    submit,
    regenerate,
    complete,
  };
}