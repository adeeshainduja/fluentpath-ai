import { useQuery } from "@tanstack/react-query";
import { History as HistoryIcon } from "lucide-react";

import { getHistory } from "../../services/historyApi";

export default function History() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["history"],
    queryFn: getHistory,
  });

  if (isLoading) {
    return (
      <div className="flex h-[70vh] items-center justify-center">
        <h1 className="text-xl font-semibold text-[#3D348B]">
          Loading history...
        </h1>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex h-[70vh] items-center justify-center">
        <h1 className="text-xl font-semibold text-red-500">
          Failed to load history.
        </h1>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-[#3D348B]">
          History
        </h1>
        <p className="mt-2 text-gray-500">
          Revisit previous writing and speaking practice sessions.
        </p>
      </div>

      <section className="space-y-4">
        {data.items.length === 0 ? (
          <div className="rounded-3xl bg-white p-8 text-gray-500 shadow-sm">
            No practice history yet.
          </div>
        ) : (
          data.items.map((item) => (
            <article
              className="rounded-3xl bg-white p-6 shadow-sm"
              key={item.record_id}
            >
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div className="flex gap-3">
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-[#D0E6FF] text-[#3D348B]">
                    <HistoryIcon size={20} />
                  </div>
                  <div>
                    <h2 className="text-xl font-bold capitalize text-[#3D348B]">
                      {item.practice_type.replaceAll("_", " ")}
                    </h2>
                    <p className="text-sm text-gray-500">
                      {new Date(item.created_at).toLocaleString()}
                    </p>
                  </div>
                </div>

                {item.score !== null &&
                  item.score !== undefined && (
                    <div className="rounded-2xl bg-[#F5F6FC] px-5 py-3 text-center">
                      <p className="text-xs font-semibold text-gray-500">
                        Score
                      </p>
                      <p className="text-2xl font-bold text-[#3D348B]">
                        {item.score}
                      </p>
                    </div>
                  )}
              </div>

              <p className="mt-5 whitespace-pre-line rounded-2xl bg-[#F5F6FC] p-4 leading-7">
                {item.submitted_text}
              </p>

              {item.feedback && (
                <p className="mt-4 rounded-2xl border border-gray-100 p-4 leading-7 text-gray-600">
                  {item.feedback}
                </p>
              )}

              <div className="mt-4 grid gap-3 md:grid-cols-4">
                <Metric
                  label="Grammar"
                  value={item.grammar_score}
                />
                <Metric
                  label="Vocabulary"
                  value={item.vocabulary_score}
                />
                <Metric
                  label="Fluency"
                  value={item.fluency_score}
                />
                <Metric
                  label="Pronunciation"
                  value={item.pronunciation_score}
                />
              </div>
            </article>
          ))
        )}
      </section>
    </div>
  );
}

function Metric({
  label,
  value,
}: {
  label: string;
  value?: number | null;
}) {
  return (
    <div className="rounded-2xl bg-[#F5F6FC] p-4">
      <p className="text-sm text-gray-500">{label}</p>
      <p className="mt-1 text-xl font-bold text-[#3D348B]">
        {value ?? "N/A"}
      </p>
    </div>
  );
}
