import { useState } from "react";
import { useParams } from "react-router-dom";

import { usePractice } from "../../hooks/usePractice";

import PracticeEditor from "../../components/practice/PracticeEditor";
import ActionButtons from "../../components/practice/ActionButtons";

export default function PracticeDetail() {
  const { id } = useParams();

  const {
    data,
    loading,
    error,
  } = usePractice(Number(id));

  const [answer, setAnswer] = useState("");

  const submitAnswer = () => {
    console.log("Practice ID:", id);
    console.log("User Answer:", answer);

    // TODO:
    // Call backend API here
    // POST /api/v1/practice/{id}/submit
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[70vh]">
        <h1 className="text-xl font-semibold text-[#3D348B]">
          Loading...
        </h1>
      </div>
    );
  }

  if (error) {
    console.log(error);

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
      <div className="flex items-center justify-center h-[70vh]">
        <h1 className="text-xl font-semibold">
          Practice not found.
        </h1>
      </div>
    );
  }

  return (
    <div className="space-y-8">

      {/* Page Title */}
      <div>
        <h1 className="text-4xl font-bold text-[#3D348B]">
          Practice Details
        </h1>

        <p className="text-gray-500 mt-2">
          Complete the exercise below and submit your answer for AI feedback.
        </p>
      </div>

      {/* Practice Information */}
      <div className="rounded-3xl bg-white p-8 shadow-sm">

        <h2 className="text-3xl font-bold text-[#3D348B]">
          {data.title}
        </h2>

        <div className="mt-6 grid grid-cols-2 gap-4">

          <p>
            <span className="font-semibold">
              Skill:
            </span>{" "}
            {data.target_skill.replaceAll("_", " ")}
          </p>

          <p>
            <span className="font-semibold">
              Practice Type:
            </span>{" "}
            {data.practice_type}
          </p>

          <p>
            <span className="font-semibold">
              Difficulty:
            </span>{" "}
            {data.difficulty}
          </p>

          <p>
            <span className="font-semibold">
              Status:
            </span>{" "}
            {data.status}
          </p>

        </div>

        <div className="mt-8">

          <h3 className="mb-3 text-xl font-bold text-[#3D348B]">
            Instructions
          </h3>

          <div className="rounded-2xl bg-gray-50 p-6 leading-8">
            {data.instruction}
          </div>

        </div>

      </div>

      {/* Writing Area */}
      <PracticeEditor
        value={answer}
        onChange={setAnswer}
      />

      {/* Buttons */}
      <ActionButtons
        onSubmit={submitAnswer}
      />

    </div>
  );
}