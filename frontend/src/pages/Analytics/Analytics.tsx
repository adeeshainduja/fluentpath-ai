import AnalyticsHeader from "../../components/analytics/AnalyticsHeader";
import OverallScoreCard from "../../components/analytics/OverallScoreCard";
import StatsGrid from "../../components/analytics/StatsGrid";
import SkillRadarChart from "../../components/analytics/SkillRadarChart";
import ProgressTrendChart from "../../components/analytics/ProgressTrendChart";
import WeakSkillsCard from "../../components/analytics/WeakSkillsCard";
import RecommendationCard from "../../components/analytics/RecommendationCard";
import WeeklyActivityChart from "../../components/analytics/WeeklyActivityChart";
import ErrorStatisticsCard from "../../components/analytics/ErrorStatisticsCard";
import PracticeHistoryTable from "../../components/analytics/PracticeHistoryTable";

export default function Analytics() {
  const overallScore = 82;

  const skills = {
    grammar: 80,
    vocabulary: 72,
    fluency: 88,
    pronunciation: 65,
  };

  const progressData = [
    {
      date: "Mon",
      score: 68,
    },
    {
      date: "Tue",
      score: 72,
    },
    {
      date: "Wed",
      score: 76,
    },
    {
      date: "Thu",
      score: 80,
    },
    {
      date: "Fri",
      score: 82,
    },
    {
      date: "Sat",
      score: 85,
    },
    {
      date: "Sun",
      score: 88,
    },
  ];

  const weakSkills = [
    {
      skill: "Vocabulary",
      score: 72,
      recommendation:
        "Practice advanced vocabulary exercises every day.",
      priority: "High",
    },
    {
      skill: "Pronunciation",
      score: 65,
      recommendation:
        "Complete speaking practice sessions with AI feedback.",
      priority: "Medium",
    },
  ];

  const recommendation = {
    priority_skill: "Vocabulary",
    strategy: "Vocabulary Practice",
    reason:
      "Vocabulary performance has consistently been lower than grammar and fluency.",
  };

  const weeklyActivity = [
    {
      day: "Mon",
      score: 70,
    },
    {
      day: "Tue",
      score: 90,
    },
    {
      day: "Wed",
      score: 55,
    },
    {
      day: "Thu",
      score: 85,
    },
    {
      day: "Fri",
      score: 78,
    },
    {
      day: "Sat",
      score: 95,
    },
    {
      day: "Sun",
      score: 88,
    },
  ];

  const history = [
    {
      date: "14 Jul",
      skill: "Grammar",
      score: 90,
      status: "Completed",
    },
    {
      date: "13 Jul",
      skill: "Vocabulary",
      score: 84,
      status: "Completed",
    },
    {
      date: "12 Jul",
      skill: "Speaking",
      score: 81,
      status: "Completed",
    },
  ];

  return (
    <div className="min-h-screen bg-slate-100">
      <div className="mx-auto max-w-7xl space-y-8 p-8">

        <AnalyticsHeader />

        <OverallScoreCard
          score={overallScore}
        />

        <StatsGrid
          grammar={skills.grammar}
          vocabulary={skills.vocabulary}
          fluency={skills.fluency}
          pronunciation={skills.pronunciation}
        />

        <div className="grid gap-6 lg:grid-cols-2">

          <SkillRadarChart
            grammar={skills.grammar}
            vocabulary={skills.vocabulary}
            fluency={skills.fluency}
            pronunciation={skills.pronunciation}
          />

          <ProgressTrendChart
            data={progressData}
          />

        </div>

        <div className="grid gap-6 lg:grid-cols-2">

          <WeakSkillsCard
            skills={weakSkills}
          />

          <RecommendationCard
            recommendation={recommendation}
          />

        </div>

        <div className="grid gap-6 lg:grid-cols-2">

          <WeeklyActivityChart
            days={weeklyActivity}
          />

          <ErrorStatisticsCard
            totalErrors={48}
            resolvedErrors={32}
            activeErrors={16}
          />

        </div>

        <PracticeHistoryTable
          history={history}
        />

      </div>
    </div>
  );
}