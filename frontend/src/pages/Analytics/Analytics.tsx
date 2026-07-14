import AnalyticsHeader from "../../components/analytics/AnalyticsHeader";
import OverallScoreCard from "../../components/analytics/OverallScoreCard";
import StatsGrid from "../../components/analytics/StatsGrid";
import SkillRadarChart from "../../components/analytics/SkillRadarChart";
import ProgressTrendChart from "../../components/analytics/ProgressTrendChart";
import WeakSkillsCard from "../../components/analytics/WeakSkillsCard";
import RecommendationCard from "../../components/analytics/RecommendationCard";

export default function Analytics() {
  // Temporary dummy data
  const overallScore = 82;

  const skillScores = {
    grammar: 80,
    vocabulary: 72,
    fluency: 88,
    pronunciation: 65,
  };
    const progressData = [
    { date: "Mon", score: 68 },
    { date: "Tue", score: 72 },
    { date: "Wed", score: 75 },
    { date: "Thu", score: 79 },
    { date: "Fri", score: 82 },
    { date: "Sat", score: 84 },
    { date: "Sun", score: 87 },
    ];
    const weakSkills = [
    {
        skill: "Vocabulary",
        score: 72,
        recommendation:
        "Practice advanced vocabulary exercises.",
        priority: "High",
    },
    {
        skill: "Pronunciation",
        score: 65,
        recommendation:
        "Complete speaking practice sessions.",
        priority: "Medium",
    },
    ];
    const recommendation = {
    strategy: "Vocabulary Practice",
    priority_skill: "Vocabulary",
    reason:
        "Vocabulary has been consistently below your grammar and fluency scores over the last five sessions.",
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
        <div className="grid gap-6 lg:grid-cols-2">
        <SkillRadarChart
            grammar={80}
            vocabulary={72}
            fluency={88}
            pronunciation={65}
        />

        <div className="rounded-3xl bg-white p-6 shadow-sm flex items-center justify-center">
            <p className="text-gray-400">
            Progress Trend Chart (Coming Next)
            </p>
        </div>
        </div>
        <div className="grid gap-6 lg:grid-cols-2">
        <SkillRadarChart
            grammar={80}
            vocabulary={72}
            fluency={88}
            pronunciation={65}
        />

        <ProgressTrendChart
            data={progressData}
        />
        </div>
        <div className="grid gap-6 lg:grid-cols-2">
        <WeakSkillsCard skills={weakSkills} />

        <div className="rounded-3xl bg-white p-6 shadow-sm flex items-center justify-center">
            <p className="text-gray-400">
            AI Recommendation Card (Coming Next)
            </p>
        </div>
        </div>
        <div className="grid gap-6 lg:grid-cols-2">
        <WeakSkillsCard skills={weakSkills} />

        <RecommendationCard
            recommendation={recommendation}
        />
        </div>

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