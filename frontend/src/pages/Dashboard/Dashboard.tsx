import SummaryGrid from "../../components/dashboard/SummaryGrid";
import RecommendationCard from "../../components/dashboard/RecommendationCard";
import GoalCard from "../../components/dashboard/GoalCard";

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

      <div className="grid grid-cols-2 gap-8">

        <RecommendationCard />

        <GoalCard />

      </div>

    </div>
  );
}