import SummaryCard from "./SummaryCard";
import type { DashboardSummary } from "../../types/dashboard";

interface SummaryGridProps {
  summary: DashboardSummary;
}

export default function SummaryGrid({
  summary,
}: SummaryGridProps) {
  return (
    <div className="grid grid-cols-4 gap-6">
      <SummaryCard
        title="Average Score"
        value={`${summary.average_score}%`}
        subtitle={summary.learning_trend}
      />

      <SummaryCard
        title="Completed Tasks"
        value={summary.completed_tasks}
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
