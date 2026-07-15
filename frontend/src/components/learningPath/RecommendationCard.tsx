import { Sparkles, ArrowRight } from "lucide-react";
import { useNavigate } from "react-router-dom";

type Props = {
  id: number;
  title: string;
  skill: string;
  difficulty: string;
  estimatedMinutes: number;
  reason: string;
};

export default function RecommendationCard({
  id,
  title,
  skill,
  difficulty,
  estimatedMinutes,
  reason,
}: Props) {
  const navigate = useNavigate();

  const handleStartPractice = () => {
    navigate(`/practice/${id}`);
  };

  return (
    <div className="bg-white rounded-3xl shadow-sm border border-gray-100 p-6">

      {/* Header */}
      <div className="flex items-center gap-3 mb-6">

        <div className="w-12 h-12 rounded-xl bg-yellow-100 flex items-center justify-center">
          <Sparkles
            className="text-yellow-500"
            size={24}
          />
        </div>

        <div>
          <h2 className="text-xl font-bold text-[#3D348B]">
            Today's Recommendation
          </h2>

          <p className="text-gray-500 text-sm">
            AI selected your next learning activity.
          </p>
        </div>

      </div>

      {/* Lesson */}
      <div className="space-y-4">

        <h3 className="text-2xl font-bold text-gray-800">
          {title}
        </h3>

        <div className="flex flex-wrap gap-3">

          <span className="px-3 py-1 rounded-full bg-blue-100 text-blue-700 text-sm font-medium">
            {skill}
          </span>

          <span className="px-3 py-1 rounded-full bg-green-100 text-green-700 text-sm font-medium">
            {difficulty}
          </span>

          <span className="px-3 py-1 rounded-full bg-purple-100 text-purple-700 text-sm font-medium">
            {estimatedMinutes} min
          </span>

        </div>

        {/* Reason */}
        <div className="rounded-xl bg-gray-50 border border-gray-100 p-4">

          <p className="text-sm leading-6 text-gray-600">

            <span className="font-semibold text-[#3D348B]">
              Why this lesson?
            </span>

            <br />

            {reason}

          </p>

        </div>

        {/* Button */}
        <button
          onClick={handleStartPractice}
          className="mt-2 w-full rounded-xl bg-[#3D348B] hover:bg-[#2f286d] transition-all duration-300 text-white font-semibold py-3 flex items-center justify-center gap-2"
        >
          Start Practice

          <ArrowRight size={18} />
        </button>

      </div>

    </div>
  );
}