import { useState } from "react";
import { useParams } from "react-router-dom";

import { usePractice } from "../../hooks/usePractice";
import { usePracticeActions } from "../../hooks/usePracticeActions";

import PracticeEditor from "../../components/practice/PracticeEditor";
import ActionButtons from "../../components/practice/ActionButtons";
import AIFeedback from "../../components/practice/AIFeedback";

interface FeedbackResult {
  score: number;
  grammar_score: number;
  vocabulary_score: number;
  fluency_score: number;
  pronunciation_score?: number | null;
  feedback: string;
  suggestions?: string[];
}

export default function PracticeDetail() {
  const { id } = useParams();

  const {
    data,
    loading,
    error,
  } = usePractice(Number(id));

  const {
    loading: actionLoading,
    submit,
    regenerate,
    complete,
  } = usePracticeActions();

  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState<FeedbackResult | null>(null);
  const [message, setMessage] = useState("");

  const submitAnswer = async () => {
    if (!id) return;

    if (!answer.trim()) {
      alert("Please write your answer before submitting.");
      return;
    }

    try {
      const result = await submit(Number(id), answer);

      console.log(result);

      if (result.result) {
        setFeedback(result.result);
      }

      if (result.message) {
        setMessage(result.message);
      } else {
        setMessage("Practice submitted successfully.");
      }
    } catch (err) {
      console.error(err);
      setMessage("Failed to submit practice.");
    }
  };

  const regenerateTask = async () => {
    if (!id) return;

    try {
      const result = await regenerate(Number(id));

      console.log(result);

      setFeedback(null);
      setAnswer("");
      setMessage(result.message ?? "Practice regenerated.");
    } catch (err) {
      console.error(err);
      setMessage("Failed to regenerate practice.");
    }
  };

  const completeTask = async () => {
    if (!id) return;

    try {
      const result = await complete(Number(id));

      console.log(result);

      setMessage(result.message ?? "Practice completed.");
    } catch (err) {
      console.error(err);
      setMessage("Failed to complete practice.");
    }
  };

  if (loading) {
    return (
      <div className="flex h-[70vh] items-center justify-center">
        <h1 className="text-xl font-semibold text-[#3D348B]">
          Loading...
        </h1>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8">
        <h1 className="text-xl text-red-600">
          Error loading practice
        </h1>

        <pre className="mt-4 overflow-auto rounded-xl bg-gray-100 p-4 text-sm">
          {JSON.stringify(error, null, 2)}
        </pre>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex h-[70vh] items-center justify-center">
        <h1 className="text-xl font-semibold">
          Practice not found.
        </h1>
      </div>
    );
  }

  return (
    <div className="space-y-8">

      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-[#3D348B]">
          Practice Details
        </h1>

        <p className="mt-2 text-gray-500">
          Complete the exercise below and submit your answer for AI feedback.
        </p>
      </div>

      {/* Success Message */}
      {message && (
        <div className="rounded-xl border border-green-200 bg-green-50 p-4 text-green-700">
          {message}
        </div>
      )}

      {/* Practice Card */}
      <div className="rounded-3xl bg-white p-8 shadow-sm">

        <h2 className="text-3xl font-bold text-[#3D348B]">
          {data.title}
        </h2>

        <div className="mt-6 grid grid-cols-2 gap-4">

          <p>
            <span className="font-semibold">Skill:</span>{" "}
            {data.target_skill.replaceAll("_", " ")}
          </p>

          <p>
            <span className="font-semibold">Practice Type:</span>{" "}
            {data.practice_type}
          </p>

          <p>
            <span className="font-semibold">Difficulty:</span>{" "}
            {data.difficulty}
          </p>

          <p>
            <span className="font-semibold">Status:</span>{" "}
            {data.status}
          </p>

        </div>

        <div className="mt-8">

          <h3 className="mb-3 text-xl font-bold text-[#3D348B]">
            Instructions
          </h3>

          <div className="rounded-2xl bg-gray-50 p-6 leading-8 whitespace-pre-line">
            {data.instruction}
          </div>

        </div>

      </div>

      {/* Writing Editor */}
      <PracticeEditor
        value={answer}
        onChange={setAnswer}
      />

      {/* Action Buttons */}
      <ActionButtons
        onSubmit={submitAnswer}
        onRegenerate={regenerateTask}
        onComplete={completeTask}
        loading={actionLoading}
      />

      {/* AI Feedback */}
      {feedback && (
        <AIFeedback
          result={feedback}
        />
      )}

    </div>
  );
}