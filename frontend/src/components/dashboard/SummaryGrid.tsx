import SummaryCard from "./SummaryCard";
import type { DashboardResponse } from "../../types/dashboard";

interface SummaryGridProps {
  dashboard: DashboardResponse;
}

export default function SummaryGrid({ dashboard }: SummaryGridProps) {
  return (
    <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
      <SummaryCard
        title="Average Score"
        value={`${dashboard.average_score}%`}
        subtitle="All completed attempts"
      />

      <SummaryCard
        title="Daily Streak"
        value={`${dashboard.daily_streak} days`}
      />

      <SummaryCard
        title="Total Practices"
        value={dashboard.total_practices}
      />

      <SummaryCard
        title="This Week"
        value={dashboard.completed_practices_this_week}
      />

      <SummaryCard
        title="Reading"
        value={`${dashboard.reading_score}%`}
      />

      <SummaryCard
        title="Listening"
        value={`${dashboard.listening_score}%`}
      />
    </div>
  );
}
