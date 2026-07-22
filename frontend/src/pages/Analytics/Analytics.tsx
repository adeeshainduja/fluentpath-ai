import {
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  BarChart,
  Bar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import type { ReactNode } from "react";
import { useAnalytics } from "../../hooks/useAnalytics";

const COLORS = ["#3D348B", "#4CB1FF", "#22C55E", "#F59E0B", "#EF4444"];

function Card({
  title,
  value,
  subtitle,
}: {
  title: string;
  value: string | number;
  subtitle?: string;
}) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <p className="text-sm font-medium uppercase tracking-wide text-slate-500">
        {title}
      </p>
      <div className="mt-3 text-3xl font-bold text-slate-900">{value}</div>
      {subtitle ? (
        <p className="mt-2 text-sm text-slate-500">{subtitle}</p>
      ) : null}
    </div>
  );
}

function ChartShell({
  title,
  children,
}: {
  title: string;
  children: ReactNode;
}) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-900">{title}</h2>
      <div className="mt-4 h-80">{children}</div>
    </section>
  );
}

export default function Analytics() {
  const { data, isLoading, error } = useAnalytics();

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-100 text-slate-600">
        Loading analytics...
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-100 text-red-600">
        Failed to load analytics.
      </div>
    );
  }

  const distributionData = data.practice_type_distribution.map((item) => ({
    name: item.practice_type,
    value: item.count,
  }));

  const radarData = [
    { skill: "Reading", score: data.reading_accuracy },
    { skill: "Listening", score: data.listening_accuracy },
    { skill: "Speaking", score: data.speaking_accuracy },
    { skill: "Writing", score: data.writing_accuracy },
    { skill: "Vocabulary", score: data.vocabulary_accuracy },
  ];

  const streakLabel =
    data.daily_streak === 1 ? "day" : "days";

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-100 to-slate-50">
      <div className="mx-auto max-w-7xl space-y-8 p-6 md:p-8">
        <header className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
          <div className="max-w-3xl">
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-[#3D348B]">
              Learner Analytics
            </p>
            <h1 className="mt-3 text-4xl font-bold text-slate-950 md:text-5xl">
              Your learning intelligence dashboard
            </h1>
            <p className="mt-4 text-lg text-slate-600">
              Real-time insights from Reading, Listening, Speaking, Writing, and
              Vocabulary practice sessions.
            </p>
          </div>
        </header>

        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <Card title="Average Score" value={`${data.average_score}%`} subtitle="Across all completed practice sessions" />
          <Card title="Total Practices" value={data.total_practices} subtitle="Completed attempts recorded" />
          <Card title="Daily Streak" value={`${data.daily_streak} ${streakLabel}`} subtitle="Current consistency run" />
          <Card title="Practice Minutes" value={data.practice_minutes} subtitle="Estimated total active learning time" />
        </section>

        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <Card title="Weekly Progress" value={`${data.weekly_progress > 0 ? "+" : ""}${data.weekly_progress}%`} subtitle="Change versus the previous week" />
          <Card title="Monthly Progress" value={`${data.monthly_progress > 0 ? "+" : ""}${data.monthly_progress}%`} subtitle="Change versus the previous month" />
          <Card title="Weakest Skill" value={data.weakest_skill} subtitle="Needs additional practice" />
          <Card title="Strongest Skill" value={data.strongest_skill} subtitle="Leading current performance" />
        </section>

        <section className="grid gap-4 lg:grid-cols-2">
          <ChartShell title="Weekly Trend">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data.weekly_score_trend}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                <XAxis dataKey="period" tickLine={false} axisLine={false} />
                <YAxis tickLine={false} axisLine={false} />
                <Tooltip />
                <Line type="monotone" dataKey="average_score" stroke="#3D348B" strokeWidth={3} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </ChartShell>

          <ChartShell title="Monthly Trend">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data.monthly_score_trend}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                <XAxis dataKey="period" tickLine={false} axisLine={false} />
                <YAxis tickLine={false} axisLine={false} />
                <Tooltip />
                <Line type="monotone" dataKey="average_score" stroke="#4CB1FF" strokeWidth={3} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </ChartShell>
        </section>

        <section className="grid gap-4 lg:grid-cols-2">
          <ChartShell title="Skill Comparison">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid />
                <PolarAngleAxis dataKey="skill" />
                <Radar dataKey="score" stroke="#22C55E" fill="#22C55E" fillOpacity={0.3} />
              </RadarChart>
            </ResponsiveContainer>
          </ChartShell>

          <ChartShell title="Practice Distribution">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={distributionData} dataKey="value" nameKey="name" outerRadius={120} label>
                  {distributionData.map((entry, index) => (
                    <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </ChartShell>
        </section>

        <section className="grid gap-4 lg:grid-cols-2">
          <ChartShell title="Progress Timeline">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data.progress_timeline}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                <XAxis dataKey="date" tickLine={false} axisLine={false} />
                <YAxis tickLine={false} axisLine={false} />
                <Tooltip />
                <Line type="monotone" dataKey="score" stroke="#F59E0B" strokeWidth={3} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </ChartShell>

          <ChartShell title="Daily Activity">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.daily_activity}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                <XAxis dataKey="date" tickLine={false} axisLine={false} />
                <YAxis tickLine={false} axisLine={false} />
                <Tooltip />
                <Bar dataKey="practice_count" fill="#3D348B" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </ChartShell>
        </section>

        <section className="grid gap-4 xl:grid-cols-3">
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm xl:col-span-2">
            <h2 className="text-lg font-semibold text-slate-900">
              Learner Insights
            </h2>
            <div className="mt-4 space-y-3">
              {data.insights.length > 0 ? (
                data.insights.map((insight) => (
                  <div key={insight} className="rounded-2xl bg-slate-50 px-4 py-3 text-slate-700">
                    {insight}
                  </div>
                ))
              ) : (
                <div className="rounded-2xl bg-slate-50 px-4 py-3 text-slate-500">
                  Keep practicing to generate more personalized insights.
                </div>
              )}
            </div>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900">
              Recent Improvement
            </h2>
            <div className="mt-4 text-4xl font-bold text-[#3D348B]">
              {data.recent_improvement > 0 ? "+" : ""}
              {data.recent_improvement}%
            </div>
            <p className="mt-3 text-sm text-slate-500">
              Recent completed practices compared with your earlier baseline.
            </p>
            <div className="mt-6 space-y-3">
              {data.recent_attempts.slice(0, 5).map((attempt) => (
                <div
                  key={`${String(attempt.title)}-${String(attempt.date)}`}
                  className="rounded-2xl border border-slate-100 bg-slate-50 px-4 py-3"
                >
                  <div className="text-sm font-semibold text-slate-900">
                    {String(attempt.title ?? "Practice")}
                  </div>
                  <div className="text-xs text-slate-500">
                    {String(attempt.practice_type ?? "practice")} -{" "}
                    {String(attempt.date ?? "")}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
