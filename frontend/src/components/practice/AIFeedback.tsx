type AIFeedbackProps = {
  result: {
    score: number;
    grammar_score: number;
    vocabulary_score: number;
    fluency_score: number;
    feedback: string;
    suggestions?: string[];
  };
};

export default function AIFeedback({
  result,
}: AIFeedbackProps) {
  return (
    <div className="rounded-3xl bg-white p-8 shadow-sm">

      <h2 className="mb-6 text-2xl font-bold text-[#3D348B]">
        AI Feedback
      </h2>

      <div className="grid grid-cols-2 gap-6">

        <div className="rounded-xl bg-blue-50 p-4">
          <h3 className="font-semibold">Overall Score</h3>
          <p className="mt-2 text-4xl font-bold text-blue-600">
            {result.score}
          </p>
        </div>

        <div className="rounded-xl bg-green-50 p-4">
          <h3 className="font-semibold">Grammar</h3>
          <p className="mt-2 text-3xl font-bold text-green-600">
            {result.grammar_score}
          </p>
        </div>

        <div className="rounded-xl bg-yellow-50 p-4">
          <h3 className="font-semibold">Vocabulary</h3>
          <p className="mt-2 text-3xl font-bold text-yellow-600">
            {result.vocabulary_score}
          </p>
        </div>

        <div className="rounded-xl bg-purple-50 p-4">
          <h3 className="font-semibold">Fluency</h3>
          <p className="mt-2 text-3xl font-bold text-purple-600">
            {result.fluency_score}
          </p>
        </div>

      </div>

      <div className="mt-8">
        <h3 className="font-semibold text-lg">
          Feedback
        </h3>

        <p className="mt-3 rounded-xl bg-gray-50 p-5">
          {result.feedback}
        </p>
      </div>

      {result.suggestions &&
        result.suggestions.length > 0 && (
          <div className="mt-8">
            <h3 className="font-semibold text-lg">
              Suggestions
            </h3>

            <ul className="mt-3 list-disc space-y-2 pl-6">
              {result.suggestions.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          </div>
      )}

    </div>
  );
}