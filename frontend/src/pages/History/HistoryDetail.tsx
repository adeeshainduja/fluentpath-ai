import type { ReactNode } from "react";
import { useQuery } from "@tanstack/react-query";
import { useParams, Link } from "react-router-dom";

import { getHistoryDetail } from "../../services/historyApi";

export default function HistoryDetail() {
  const { attemptId } = useParams();
  const id = Number(attemptId);

  const { data, isLoading, error } = useQuery({
    queryKey: ["history-detail", id],
    queryFn: () => getHistoryDetail(id),
    enabled: Number.isFinite(id),
  });

  if (isLoading) return <div className="p-8">Loading details...</div>;
  if (error || !data) return <div className="p-8 text-red-500">Failed to load history details.</div>;

  const history = data.history;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-[#3D348B]">{history.title}</h1>
          <p className="text-gray-500 capitalize">{history.practice_type} • {new Date(history.completed_date).toLocaleString()}</p>
        </div>
        <Link className="rounded-full border px-4 py-2" to="/history">Back</Link>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Panel title="Original Practice">{JSON.stringify(history.original_practice, null, 2)}</Panel>
        <Panel title="Learner Answers">{JSON.stringify(history.learner_answers, null, 2)}</Panel>
        <Panel title="Correct Answers">{JSON.stringify(history.correct_answers ?? {}, null, 2)}</Panel>
        <Panel title="Explanation & Feedback">{history.feedback_summary ?? history.ai_feedback ?? "No feedback available."}</Panel>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Panel title="Strengths">{history.strengths.join("\n") || "No strengths recorded."}</Panel>
        <Panel title="Weaknesses">{history.weaknesses.join("\n") || "No weaknesses recorded."}</Panel>
      </div>
    </div>
  );
}

function Panel({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section className="rounded-3xl bg-white p-6 shadow-sm">
      <h2 className="mb-3 text-lg font-semibold text-[#3D348B]">{title}</h2>
      <pre className="whitespace-pre-wrap break-words text-sm text-gray-700">{children}</pre>
    </section>
  );
}
