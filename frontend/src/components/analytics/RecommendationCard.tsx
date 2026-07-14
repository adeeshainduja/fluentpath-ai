interface Recommendation {
  strategy: string;
  priority_skill: string;
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
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-white/20 text-2xl">
          🤖
        </div>

        <div>
          <h2 className="text-2xl font-bold">
            AI Recommendation
          </h2>

          <p className="text-sm text-white/80">
            Personalized learning advice
          </p>
        </div>
      </div>

      <div className="mt-8">
        <p className="text-lg">
          Focus on{" "}
          <span className="font-bold">
            {recommendation.priority_skill}
          </span>{" "}
          this week.
        </p>
      </div>

      <div className="mt-6 rounded-2xl bg-white/10 p-5">
        <p className="text-sm text-white/70">
          Strategy
        </p>

        <p className="mt-1 text-lg font-semibold capitalize">
          {recommendation.strategy.replaceAll("_", " ")}
        </p>

        <div className="mt-5">
          <p className="text-sm text-white/70">
            Reason
          </p>

          <p className="mt-1 leading-7">
            {recommendation.reason}
          </p>
        </div>
      </div>

      <button className="mt-8 rounded-xl bg-white px-6 py-3 font-semibold text-[#3D348B] transition hover:bg-gray-100">
        Start Practice
      </button>
    </div>
  );
}