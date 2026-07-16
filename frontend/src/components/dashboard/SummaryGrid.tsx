import SummaryCard from "./SummaryCard";
import type { DashboardSummary } from "../../types/dashboard";

interface SummaryGridProps {
  summary: DashboardSummary;
}

export default function SummaryGrid({
  summary,
}: SummaryGridProps) {
  return (
    <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-5">
      <SummaryCard
        title="Average Score"
        value={`${summary.average_score}%`}
        subtitle={summary.learning_trend}
      />

      <SummaryCard
        title="Daily Streak"
        value={`${summary.daily_streak} days`}
      />

      <SummaryCard
        title="Total Practices"
        value={summary.total_practices}
      />

      <SummaryCard
        title="Current Focus"
        value={summary.recommended_skill ?? "No data"}
      />

      <SummaryCard
        title="Strategy"
        value={
          summary.recommended_strategy?.replaceAll("_", " ") ??
          "No data"
        }
      />
    </div>
  );
}
