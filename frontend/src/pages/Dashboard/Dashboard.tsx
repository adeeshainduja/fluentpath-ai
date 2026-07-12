import SummaryGrid from "../../components/dashboard/SummaryGrid";
import RecommendationCard from "../../components/dashboard/RecommendationCard";
import GoalCard from "../../components/dashboard/GoalCard";
import ProgressChart from "../../components/dashboard/ProgressChart";
import SkillRadar from "../../components/dashboard/SkillRadar";

export default function Dashboard() {
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

      {/* Summary */}

      <SummaryGrid />

      {/* AI Section */}

      <div className="grid grid-cols-3 gap-8">

        <div className="col-span-2">
            <ProgressChart />
        </div>

        <RecommendationCard />

        </div>

        <div className="grid grid-cols-2 gap-8">

        <GoalCard />

        <div className="grid grid-cols-2 gap-8">

        <SkillRadar />

        <GoalCard />

        </div>


    </div>

    </div>
  );
}