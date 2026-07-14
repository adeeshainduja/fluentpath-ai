import AnalyticsHeader from "../../components/analytics/AnalyticsHeader";
import OverallScoreCard from "../../components/analytics/OverallScoreCard";
import StatsGrid from "../../components/analytics/StatsGrid";

export default function Analytics() {
  // Temporary dummy data
  const overallScore = 82;

  const skillScores = {
    grammar: 80,
    vocabulary: 72,
    fluency: 88,
    pronunciation: 65,
  };

  return (
    <div className="min-h-screen bg-slate-100 p-8">
      <div className="mx-auto max-w-7xl space-y-8">
        <AnalyticsHeader />

        <OverallScoreCard score={overallScore} />

        <StatsGrid
          grammar={skillScores.grammar}
          vocabulary={skillScores.vocabulary}
          fluency={skillScores.fluency}
          pronunciation={skillScores.pronunciation}
        />

        {/* Next components will be added here */}

        {/*
        <SkillRadarChart />

        <ProgressTrendChart />

        <div className="grid gap-6 lg:grid-cols-2">
            <WeakSkillsCard />
            <RecommendationCard />
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
            <WeeklyActivityChart />
            <ErrorStatisticsCard />
        </div>

        <PracticeHistoryTable />
        */}
      </div>
    </div>
  );
}