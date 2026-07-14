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

import { useDashboard } from "../../hooks/useDashboard";

export default function Analytics() {
  const learnerId = 1;

  const {
    data,
    isLoading,
    error,
  } = useDashboard(learnerId);

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        Loading analytics...
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex h-screen items-center justify-center text-red-500">
        Failed to load analytics.
      </div>
    );
  }

  const getSkillScore = (skill: string) =>
    data.skill_progress.find(
      (item: { skill: string; }) =>
        item.skill.toLowerCase() ===
        skill.toLowerCase()
    )?.average_score ?? 0;

  const progressData =
    data.learning_timeline.map(
      (item: { date: string; average_score: number }) => ({
        date: item.date,
        score: item.average_score,
      })
    );

  const weeklyActivity =
    data.learning_timeline.map(
      (item: { date: string; average_score: number }) => ({
        day: new Date(
          item.date
        ).toLocaleDateString(
          "en-US",
          {
            weekday: "short",
          }
        ),
        score: item.average_score,
      })
    );

  const history =
    data.practice_history.map(
      (item: { created_at: string; target_skill: string; task_score: number | undefined; status: string | undefined }) => ({
        date: new Date(
          item.created_at
        ).toLocaleDateString(),

        skill:
          item.target_skill,

        score:
          item.task_score ?? 0,

        status:
          item.status ??
          "Completed",
      })
    );

  return (
    <div className="min-h-screen bg-slate-100">
      <div className="mx-auto max-w-7xl space-y-8 p-8">

        <AnalyticsHeader />

        <OverallScoreCard
          score={
            data.summary.average_score
          }
        />

        <StatsGrid
          grammar={getSkillScore(
            "Grammar"
          )}
          vocabulary={getSkillScore(
            "Vocabulary"
          )}
          fluency={getSkillScore(
            "Fluency"
          )}
          pronunciation={getSkillScore(
            "Pronunciation"
          )}
        />

        <div className="grid gap-6 lg:grid-cols-2">

          <SkillRadarChart
            grammar={getSkillScore(
              "Grammar"
            )}
            vocabulary={getSkillScore(
              "Vocabulary"
            )}
            fluency={getSkillScore(
              "Fluency"
            )}
            pronunciation={getSkillScore(
              "Pronunciation"
            )}
          />

          <ProgressTrendChart
            data={progressData}
          />

        </div>
                <div className="grid gap-6 lg:grid-cols-2">

          <WeakSkillsCard
            skills={data.weak_skills}
          />

          <RecommendationCard
            recommendation={{
              priority_skill:
                data.recommendations.priority_skill ??
                data.recommendations.selected_skill ??
                "General",

              strategy:
                data.recommendations.strategy,

              reason:
                data.recommendations.reason,
            }}
          />

        </div>

        <div className="grid gap-6 lg:grid-cols-2">

          <WeeklyActivityChart
            days={weeklyActivity}
          />

          <ErrorStatisticsCard
            totalErrors={
              data.error_statistics.total_errors
            }
            resolvedErrors={
              data.error_statistics.resolved_errors ??
              0
            }
            activeErrors={
              data.error_statistics.active_errors ??
              0
            }
          />

        </div>

        <PracticeHistoryTable
          history={history}
        />

      </div>
    </div>
  );
}