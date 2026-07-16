import { useDashboard } from "../../hooks/useDashboard";

import SummaryGrid from "../../components/dashboard/SummaryGrid";
import RecommendationCard from "../../components/dashboard/RecommendationCard";
import GoalCard from "../../components/dashboard/GoalCard";
import ProgressChart from "../../components/dashboard/ProgressChart";
import SkillRadar from "../../components/dashboard/SkillRadar";
import PracticeHistory from "../../components/dashboard/PracticeHistory";
import DailyMission from "../../components/dashboard/DailyMission";
import AchievementBadges from "../../components/dashboard/AchievementBadges";
import WeakSkills from "../../components/dashboard/WeakSkills";
import { useAuth } from "../../hooks/useAuth";

export default function Dashboard() {
  const { user } = useAuth();
  const { data, isLoading, error } = useDashboard();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-[70vh]">
        <h1 className="text-xl font-semibold text-[#3D348B]">
          Loading...
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

  const strongSkills = [...data.skill_progress]
    .sort(
      (first, second) =>
        second.average_score - first.average_score
    )
    .slice(0, 3);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-[#3D348B]">
          Dashboard
        </h1>

        <p className="text-gray-500">
          Welcome back, {user?.full_name ?? "learner"}. Here's your learning overview.
        </p>
      </div>

      {/* Summary Cards */}
      <SummaryGrid summary={data.summary} />

      {/* Progress + AI Recommendation */}
      <div className="grid grid-cols-3 gap-8">
        <div className="col-span-2">
          <ProgressChart timeline={data.learning_timeline} />
        </div>

        <RecommendationCard recommendation={data.recommendations} />
      </div>

      {/* Skills + Goal */}
      <div className="grid grid-cols-3 gap-8">
        <div className="col-span-2">
          <SkillRadar skills={data.skill_progress} />
        </div>

        <GoalCard />
      </div>

      {/* Practice History */}
      <PracticeHistory history={data.practice_history} />

      {/* Daily Mission & Achievements */}
      <div className="grid grid-cols-2 gap-8">
        <DailyMission missions={data.daily_missions} />
        <AchievementBadges badges={data.achievement_badges} />
      </div>
      <WeakSkills skills={data.weak_skills} />

      <section className="rounded-2xl bg-white p-6 shadow-sm">
        <h2 className="text-xl font-bold text-[#3D348B]">
          Strong Skills
        </h2>
        <div className="mt-4 grid gap-4 md:grid-cols-3">
          {strongSkills.length === 0 ? (
            <p className="text-gray-500">
              Complete a few evaluated practices to reveal your strongest skills.
            </p>
          ) : (
            strongSkills.map((skill) => (
              <div
                className="rounded-xl bg-[#F5F6FC] p-4"
                key={skill.skill}
              >
                <p className="font-semibold capitalize text-[#4A4B4B]">
                  {skill.skill}
                </p>
                <p className="mt-2 text-2xl font-bold text-[#3D348B]">
                  {skill.average_score}%
                </p>
              </div>
            ))
          )}
        </div>
      </section>
    </div>
  );
}
