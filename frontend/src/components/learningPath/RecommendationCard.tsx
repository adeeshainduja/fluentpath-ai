import { Sparkles, ArrowRight } from "lucide-react";

type Props = {
  title: string;
  skill: string;
  difficulty: string;
  estimatedMinutes: number;
  reason: string;
};

export default function RecommendationCard({
  title,
  skill,
  difficulty,
  estimatedMinutes,
  reason,
}: Props) {
  return (
    <div className="bg-white rounded-3xl shadow-sm border border-gray-100 p-6">

      <div className="flex items-center gap-3 mb-5">
        <div className="w-12 h-12 rounded-xl bg-yellow-100 flex items-center justify-center">
          <Sparkles className="text-yellow-500" size={24} />
        </div>

        <div>
          <h2 className="text-xl font-bold text-[#3D348B]">
            Today's Recommendation
          </h2>

          <p className="text-gray-500 text-sm">
            AI selected your next lesson.
          </p>
        </div>
      </div>

      <div className="space-y-3">

        <h3 className="text-2xl font-bold text-gray-800">
          {title}
        </h3>

        <div className="flex gap-3 flex-wrap">

          <span className="px-3 py-1 rounded-full bg-blue-100 text-blue-700 text-sm">
            {skill}
          </span>

          <span className="px-3 py-1 rounded-full bg-green-100 text-green-700 text-sm">
            {difficulty}
          </span>

          <span className="px-3 py-1 rounded-full bg-purple-100 text-purple-700 text-sm">
            {estimatedMinutes} min
          </span>

        </div>

        <div className="mt-4 rounded-xl bg-gray-50 p-4">

          <p className="text-sm text-gray-600">

            <span className="font-semibold text-[#3D348B]">
              Why this lesson?
            </span>

            <br />

            {reason}

          </p>

        </div>

        <button className="mt-4 w-full rounded-xl bg-[#3D348B] hover:bg-[#2f286d] transition text-white font-semibold py-3 flex justify-center items-center gap-2">

          Start Practice

          <ArrowRight size={18} />

        </button>

      </div>

    </div>
  );
}