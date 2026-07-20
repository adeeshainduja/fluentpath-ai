import { useDashboard } from "../../hooks/useDashboard";
import { useAuth } from "../../hooks/useAuth";

import SummaryGrid from "../../components/dashboard/SummaryGrid";
import RecommendationCard from "../../components/dashboard/RecommendationCard";
import GoalCard from "../../components/dashboard/GoalCard";
import PracticeHistory from "../../components/dashboard/PracticeHistory";
import AchievementBadges from "../../components/dashboard/AchievementBadges";

export default function Dashboard() {
  const { user } = useAuth();
  const { data, isLoading, error } = useDashboard();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-[70vh]">
        <h1 className="text-xl font-semibold text-[#3D348B]">
          Loading dashboard...
        </h1>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex items-center justify-center h-[70vh]">
        <h1 className="text-xl font-semibold text-red-500">
          Error loading dashboard.
        </h1>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-[#3D348B]">
          Dashboard
        </h1>

        <p className="text-gray-500">
          Welcome back, {user?.full_name ?? data.learner_name}. Here&apos;s your learning overview.
        </p>
      </div>

      <SummaryGrid dashboard={data} />

      <div className="grid grid-cols-3 gap-8">
        <div className="col-span-2">
          <GoalCard dashboard={data} />
        </div>

        <RecommendationCard dashboard={data} />
      </div>

      <section className="rounded-3xl bg-white p-6 shadow-sm">
        <h2 className="text-xl font-bold text-[#3D348B]">
          Skill Scores
        </h2>
        <div className="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-5">
          {[
            ["Reading", data.reading_score],
            ["Listening", data.listening_score],
            ["Speaking", data.speaking_score],
            ["Writing", data.writing_score],
            ["Vocabulary", data.vocabulary_score],
          ].map(([label, score]) => (
            <div key={label as string} className="rounded-2xl bg-[#F5F6FC] p-4">
              <p className="text-sm text-gray-500">{label}</p>
              <p className="mt-2 text-2xl font-bold text-[#3D348B]">
                {score}%
              </p>
            </div>
          ))}
        </div>
      </section>

      <PracticeHistory latestPractice={data.latest_practice} />

      <AchievementBadges badges={data.achievements} />
    </div>
  );
}
