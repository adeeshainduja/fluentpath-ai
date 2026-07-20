import { Sparkles } from "lucide-react";
import type { DashboardResponse } from "../../types/dashboard";

interface RecommendationCardProps {
  dashboard: DashboardResponse;
}

export default function RecommendationCard({
  dashboard,
}: RecommendationCardProps) {
  return (
    <div className="rounded-3xl bg-gradient-to-br from-[#3D348B] to-[#4CB1FF] p-8 text-white shadow-lg">
      <div className="flex items-center gap-3">
        <Sparkles size={28} />
        <h2 className="text-xl font-bold">AI Recommendation</h2>
      </div>

      <p className="mt-6 leading-7 text-white/90">
        {dashboard.ai_recommendation_summary ?? "No recommendation available yet."}
      </p>

      <div className="mt-5 rounded-2xl bg-white/10 p-4">
        <p className="text-sm text-white/80">Learner</p>
        <p className="font-semibold">{dashboard.learner_name}</p>

        <p className="mt-3 text-sm text-white/80">Latest practice</p>
        <p>{dashboard.latest_practice?.title ?? "No completed practice yet"}</p>
      </div>

      <button className="mt-8 rounded-xl bg-white px-6 py-3 font-semibold text-[#3D348B]">
        Start Practice
      </button>
    </div>
  );
}
