import {
  Bot,
  Sparkles,
  TrendingUp,
  ArrowRight,
} from "lucide-react";

interface CoachPanelProps {
  message?: string;
  recommendation?: string;
}

export default function CoachPanel({
  message = "Excellent work! Your grammar has improved by 12% compared to last week. Vocabulary is now your weakest skill, so focus on Business Email Writing to continue your progress.",
  recommendation = "Business Email Writing",
}: CoachPanelProps) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">

      {/* Header */}
      <div className="mb-6 flex items-center gap-3">
        <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-[#4CB1FF] to-[#3D348B] text-white">
          <Bot size={28} />
        </div>

        <div>
          <h2 className="text-2xl font-bold text-[#3D348B]">
            AI Coach
          </h2>

          <p className="text-sm text-gray-500">
            Personalized learning guidance
          </p>
        </div>
      </div>

      {/* AI Message */}
      <div className="rounded-2xl bg-[#F8FAFF] p-5">
        <div className="mb-3 flex items-center gap-2 text-[#4CB1FF]">
          <Sparkles size={18} />
          <span className="font-semibold">
            Today's Insight
          </span>
        </div>

        <p className="leading-7 text-gray-700">
          {message}
        </p>
      </div>

      {/* Recommendation */}
      <div className="mt-6 rounded-2xl border border-blue-100 bg-gradient-to-r from-blue-50 to-indigo-50 p-5">

        <div className="mb-3 flex items-center gap-2">
          <TrendingUp
            size={20}
            className="text-[#3D348B]"
          />

          <h3 className="font-semibold text-[#3D348B]">
            Recommended Next Practice
          </h3>
        </div>

        <div className="flex items-center justify-between">

          <span className="font-medium text-gray-700">
            {recommendation}
          </span>

          <button className="flex items-center gap-2 rounded-xl bg-[#3D348B] px-4 py-2 text-sm font-medium text-white transition hover:bg-[#2f2870]">
            Start
            <ArrowRight size={16} />
          </button>

        </div>
      </div>

      {/* Progress Summary */}
      <div className="mt-6 grid grid-cols-2 gap-4">

        <div className="rounded-2xl bg-green-50 p-4 text-center">
          <p className="text-sm text-gray-500">
            Improvement
          </p>

          <h3 className="mt-1 text-2xl font-bold text-green-600">
            +12%
          </h3>
        </div>

        <div className="rounded-2xl bg-orange-50 p-4 text-center">
          <p className="text-sm text-gray-500">
            Focus Skill
          </p>

          <h3 className="mt-1 font-semibold text-orange-600">
            Vocabulary
          </h3>
        </div>

      </div>

    </div>
  );
}