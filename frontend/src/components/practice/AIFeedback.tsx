type Props = {
  feedback: any;
};

export default function AIFeedback({
  feedback,
}: Props) {
  if (!feedback) return null;

  return (
    <div className="rounded-3xl bg-white p-8 shadow-sm">

      <h2 className="text-2xl font-bold text-[#3D348B]">
        AI Feedback
      </h2>

      <div className="mt-6 grid grid-cols-2 gap-4">

        <div className="rounded-xl bg-blue-50 p-4">
          <p className="text-sm text-gray-500">
            Overall Score
          </p>

          <p className="text-3xl font-bold text-blue-600">
            {feedback.score}
          </p>
        </div>

        <div className="rounded-xl bg-green-50 p-4">
          <p className="text-sm text-gray-500">
            Grammar
          </p>

          <p className="text-2xl font-bold text-green-600">
            {feedback.grammar_score}
          </p>
        </div>

        <div className="rounded-xl bg-yellow-50 p-4">
          <p className="text-sm text-gray-500">
            Vocabulary
          </p>

          <p className="text-2xl font-bold text-yellow-600">
            {feedback.vocabulary_score}
          </p>
        </div>

        <div className="rounded-xl bg-purple-50 p-4">
          <p className="text-sm text-gray-500">
            Fluency
          </p>

          <p className="text-2xl font-bold text-purple-600">
            {feedback.fluency_score}
          </p>
        </div>

      </div>

      <div className="mt-8">

        <h3 className="font-bold text-lg text-[#3D348B]">
          Feedback
        </h3>

        <p className="mt-2 leading-8">
          {feedback.feedback}
        </p>

      </div>

      <div className="mt-8">

        <h3 className="font-bold text-lg text-[#3D348B]">
          Suggestions
        </h3>

        <ul className="mt-3 list-disc space-y-2 pl-6">
          {feedback.suggestions.map(
            (
              suggestion: string,
              index: number
            ) => (
              <li key={index}>
                {suggestion}
              </li>
            )
          )}
        </ul>

      </div>

    </div>
  );
}