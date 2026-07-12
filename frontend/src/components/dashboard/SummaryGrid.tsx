import SummaryCard from "./SummaryCard";

export default function SummaryGrid() {
  return (
    <div className="grid grid-cols-4 gap-6">
      <SummaryCard
        title="Average Score"
        value="82%"
        subtitle="+5% this week"
      />

      <SummaryCard
        title="Completed Tasks"
        value="156"
      />

      <SummaryCard
        title="Current Focus"
        value="Grammar"
      />

      <SummaryCard
        title="Learning Streak"
        value="12 Days"
      />
    </div>
  );
}