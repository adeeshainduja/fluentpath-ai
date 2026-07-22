import { Sparkles } from "lucide-react";
import { useNavigate } from "react-router-dom";
import type { AdaptivePracticeRecommendation } from "../../types/adaptivePractice";

interface RecommendationCardProps {
  recommendation: AdaptivePracticeRecommendation | null;
  learnerName: string;
}

export default function RecommendationCard({
  recommendation,
  learnerName,
}: RecommendationCardProps) {
  const navigate = useNavigate();

  return (
    <div className="rounded-3xl bg-gradient-to-br from-[#3D348B] to-[#4CB1FF] p-8 text-white shadow-lg">
      <div className="flex items-center gap-3">
        <Sparkles size={28} />
        <h2 className="text-xl font-bold">Today&apos;s Recommended Practice</h2>
      </div>

      <p className="mt-6 leading-7 text-white/90">
        {recommendation?.reason ?? "No recommendation available yet."}
      </p>

      <div className="mt-5 rounded-2xl bg-white/10 p-4">
        <p className="text-sm text-white/80">Learner</p>
        <p className="font-semibold">{learnerName}</p>

        <p className="mt-3 text-sm text-white/80">Priority</p>
        <p>{recommendation?.priority ?? "Medium"}</p>

        <p className="mt-3 text-sm text-white/80">Estimated time</p>
        <p>{recommendation?.estimatedTime ?? "15 minutes"}</p>
      </div>

      <button
        onClick={() => navigate("/practice")}
        className="mt-8 rounded-xl bg-white px-6 py-3 font-semibold text-[#3D348B]"
      >
        Start Practice
      </button>
    </div>
  );
}
