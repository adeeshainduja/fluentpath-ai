import {
  Award,
  BarChart3,
  CalendarDays,
  Flame,
  GraduationCap,
  History,
} from "lucide-react";
import { useDashboard } from "../../hooks/useDashboard";
import { useLearnerIntelligence } from "../../hooks/useLearnerIntelligence";
import { useAuth } from "../../hooks/useAuth";

const formatLabel = (value?: string | null) =>
  value ? value.replaceAll("_", " ") : "No data";

export default function Profile() {
  const { user } = useAuth();
  const learnerId = user?.id ?? 0;
  const intelligence = useLearnerIntelligence(learnerId);
  const dashboard = useDashboard();

  if (intelligence.isLoading || dashboard.isLoading) {
    return (
      <div className="flex h-[70vh] items-center justify-center">
        <h1 className="text-xl font-semibold text-[#3D348B]">
          Loading profile...
        </h1>
      </div>
    );
  }

  if (intelligence.error || dashboard.error) {
    return (
      <div className="flex h-[70vh] items-center justify-center">
        <h1 className="text-xl font-semibold text-red-500">
          Failed to load profile.
        </h1>
      </div>
    );
  }

  const data = intelligence.data;
  const dashboardData = dashboard.data;

  if (!data || !dashboardData) {
    return (
      <div className="flex h-[70vh] items-center justify-center">
        <h1 className="text-xl font-semibold text-gray-500">
          No learner data available.
        </h1>
      </div>
    );
  }

  const achievements = dashboardData.achievement_badges ?? [];
  const earnedAchievements = achievements.filter(
    (achievement) => achievement.earned
  );

  const skillScores = data.performance?.average_scores_by_skill ?? [];
  const practiceFrequency = data.performance?.practice_frequency;
  const insights = data.dashboard_insights;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-[#3D348B]">Profile</h1>
        <p className="text-gray-500">
          Learner statistics and progress summary.
        </p>
      </div>

      <section className="grid grid-cols-1 gap-6 xl:grid-cols-4">
        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3 text-[#3D348B]">
            <GraduationCap size={22} />
            <p className="text-sm text-gray-500">CEFR Level</p>
          </div>

          <h2 className="mt-3 text-3xl font-bold text-[#3D348B]">
            {insights?.current_level ?? "N/A"}
          </h2>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3 text-[#3D348B]">
            <Flame size={22} />
            <p className="text-sm text-gray-500">Practice Streak</p>
          </div>

          <h2 className="mt-3 text-3xl font-bold text-[#3D348B]">
            {insights?.practice_streak ?? 0}
          </h2>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3 text-[#3D348B]">
            <History size={22} />
            <p className="text-sm text-gray-500">Total Practices</p>
          </div>

          <h2 className="mt-3 text-3xl font-bold text-[#3D348B]">
            {practiceFrequency?.total_practices ?? 0}
          </h2>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3 text-[#3D348B]">
            <Award size={22} />
            <p className="text-sm text-gray-500">Achievements</p>
          </div>

          <h2 className="mt-3 text-3xl font-bold text-[#3D348B]">
            {earnedAchievements.length}
          </h2>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-8 xl:grid-cols-3">
        <div className="xl:col-span-2 rounded-2xl bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <BarChart3 className="text-[#3D348B]" size={24} />
            <h2 className="text-xl font-bold text-[#3D348B]">
              Skill Scores
            </h2>
          </div>

          <div className="mt-5 grid grid-cols-1 gap-4 md:grid-cols-2">
            {skillScores.length === 0 ? (
              <p className="text-gray-500">
                No evaluated skill scores are available yet.
              </p>
            ) : (
              skillScores.map((skill) => (
                <div
                  key={skill.skill}
                  className="rounded-xl border border-gray-100 p-5"
                >
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold capitalize">
                      {formatLabel(skill.skill)}
                    </h3>

                    <span className="font-bold text-[#3D348B]">
                      {skill.average_score}
                    </span>
                  </div>

                  <p className="mt-2 text-sm text-gray-500">
                    {formatLabel(skill.trend)}
                  </p>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="space-y-8">
          <div className="rounded-2xl bg-white p-6 shadow-sm">
            <div className="flex items-center gap-3">
              <CalendarDays className="text-[#3D348B]" size={22} />
              <h2 className="text-lg font-bold text-[#3D348B]">
                Practice Summary
              </h2>
            </div>

            <div className="mt-4 space-y-3">
              <div className="flex justify-between">
                <span>Active Days</span>
                <span>{practiceFrequency?.active_days ?? 0}</span>
              </div>

              <div className="flex justify-between">
                <span>Last 7 Days</span>
                <span>{practiceFrequency?.practices_last_7_days ?? 0}</span>
              </div>

              <div className="flex justify-between">
                <span>Last 30 Days</span>
                <span>{practiceFrequency?.practices_last_30_days ?? 0}</span>
              </div>

              <div className="flex justify-between">
                <span>Completed Tasks</span>
                <span>{dashboardData.summary?.completed_tasks ?? 0}</span>
              </div>
            </div>
          </div>

          <div className="rounded-2xl bg-white p-6 shadow-sm">
            <h2 className="text-lg font-bold text-[#3D348B]">
              Achievements
            </h2>

            <div className="mt-4 space-y-3">
              {achievements.length === 0 ? (
                <p className="text-gray-500">
                  No achievements available.
                </p>
              ) : (
                achievements.map((achievement) => (
                  <div
                    key={achievement.title}
                    className="rounded-lg bg-[#F5F6FC] p-4"
                  >
                    <div className="flex justify-between">
                      <h3 className="font-semibold">
                        {achievement.title}
                      </h3>

                      <span>
                        {achievement.earned ? "Earned" : "Open"}
                      </span>
                    </div>

                    <p className="mt-2 text-sm text-gray-500">
                      {achievement.description}
                    </p>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
