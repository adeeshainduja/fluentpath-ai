import { useState } from "react";

export default function ReadingPractice() {
  const [answers, setAnswers] = useState({
    q1: "",
    q2: "",
  });

  const passage = `
Yesterday Tom visited the national museum with his classmates.
He learned about ancient history and enjoyed the science exhibition.
Before going home, he bought a history book from the museum shop.
`;

  const submitAnswers = () => {
    console.log(answers);
    alert("Reading answers submitted.");
  };

  return (
    <div className="space-y-8">

      <div>
        <h1 className="text-4xl font-bold text-[#3D348B]">
          Reading Practice
        </h1>

        <p className="text-gray-500 mt-2">
          Read the passage and answer the questions.
        </p>
      </div>

      <div className="rounded-3xl bg-white p-8 shadow-sm">
        <h2 className="text-2xl font-bold text-[#3D348B] mb-4">
          Passage
        </h2>

        <p className="leading-8 whitespace-pre-line">
          {passage}
        </p>
      </div>

      <div className="rounded-3xl bg-white p-8 shadow-sm">

        <h2 className="text-xl font-bold mb-4">
          Question 1
        </h2>

        <p>Where did Tom go?</p>

        <select
          className="mt-4 border rounded-xl p-3 w-full"
          value={answers.q1}
          onChange={(e) =>
            setAnswers({
              ...answers,
              q1: e.target.value,
            })
          }
        >
          <option value="">Select</option>
          <option>Museum</option>
          <option>Library</option>
          <option>School</option>
          <option>Beach</option>
        </select>

        <h2 className="text-xl font-bold mt-8 mb-4">
          Question 2
        </h2>

        <p>What did he buy?</p>

        <select
          className="mt-4 border rounded-xl p-3 w-full"
          value={answers.q2}
          onChange={(e) =>
            setAnswers({
              ...answers,
              q2: e.target.value,
            })
          }
        >
          <option value="">Select</option>
          <option>History Book</option>
          <option>Food</option>
          <option>Shoes</option>
          <option>Pen</option>
        </select>

        <button
          onClick={submitAnswers}
          className="mt-8 bg-[#3D348B] text-white px-8 py-3 rounded-xl"
        >
          Submit Answers
        </button>

      </div>

    </div>
  );
}