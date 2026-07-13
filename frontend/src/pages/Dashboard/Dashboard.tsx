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

export default function Dashboard() {
  const { data, isLoading, error } = useDashboard(1);

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

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-[#3D348B]">
          Dashboard
        </h1>

        <p className="text-gray-500">
          Welcome back! Here's your learning overview.
        </p>
      </div>

      {/* Summary Cards */}
      <SummaryGrid summary={data.summary} />

      {/* Progress + AI Recommendation */}
      <div className="grid grid-cols-3 gap-8">
        <div className="col-span-2">
          <ProgressChart timeline={data.learning_timeline} />
        </div>

        <RecommendationCard recommendation={data.summary} />
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
        <AchievementBadges />
      </div>
      <WeakSkills skills={data.weak_skills} />
    </div>
  );
}