import SummaryCard from "./SummaryCard";

interface Summary {
  average_score: number;
  completed_tasks: number;
  pending_tasks: number;
  learning_trend: string;
  recommended_skill: string;
  recommended_strategy: string;
}

interface SummaryGridProps {
  summary: Summary;
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
        value={summary.recommended_skill}
      />

      <SummaryCard
        title="Strategy"
        value={summary.recommended_strategy.replaceAll("_", " ")}
      />
    </div>
  );
}