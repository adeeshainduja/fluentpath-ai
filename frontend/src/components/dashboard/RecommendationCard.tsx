import { Sparkles } from "lucide-react";

interface Recommendation {
  priority_skill: string;
  strategy: string;
  reason: string;
}

interface RecommendationCardProps {
  recommendation: Recommendation;
}

export default function RecommendationCard({
  recommendation,
}: RecommendationCardProps) {
  return (
    <div className="rounded-3xl bg-gradient-to-br from-[#3D348B] to-[#4CB1FF] p-8 text-white shadow-lg">
      <div className="flex items-center gap-3">
        <Sparkles size={28} />
        <h2 className="text-xl font-bold">AI Recommendation</h2>
      </div>

      <p className="mt-6 leading-7 text-white/90">
        Focus on{" "}
        <strong>
          {recommendation.priority_skill.replaceAll("_", " ")}
        </strong>{" "}
        today.
      </p>

      <div className="mt-5 rounded-2xl bg-white/10 p-4">
        <p className="text-sm text-white/80">Strategy</p>

        <p className="font-semibold capitalize">
          {recommendation.strategy.replaceAll("_", " ")}
        </p>

        <p className="mt-3 text-sm text-white/80">Reason</p>

        <p>{recommendation.reason}</p>
      </div>

      <button className="mt-8 rounded-xl bg-white px-6 py-3 font-semibold text-[#3D348B]">
        Start Practice
      </button>
    </div>
  );
}