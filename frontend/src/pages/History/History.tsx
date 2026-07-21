import { useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Filter, Search, History as HistoryIcon } from "lucide-react";

import { getHistory } from "../../services/historyApi";
import type { PracticeType } from "../../types/history";

const practiceTypes: PracticeType[] = [
  "all",
  "reading",
  "listening",
  "writing",
  "speaking",
  "vocabulary",
];

export default function History() {
  const [params, setParams] = useSearchParams();
  const [search, setSearch] = useState(params.get("search") ?? "");
  const [dateFilter, setDateFilter] = useState("");
  const page = Number(params.get("page") ?? "1");
  const limit = Number(params.get("limit") ?? "20");
  const type = (params.get("type") ?? "all") as PracticeType;
  const sort = (params.get("sort") ?? "newest") as
    | "newest"
    | "oldest"
    | "score_desc"
    | "score_asc";

  const { data, isLoading, error } = useQuery({
    queryKey: ["history", page, limit, type, sort, search],
    queryFn: () =>
      getHistory({
        page,
        limit,
        type,
        sort,
        search: search || undefined,
      }),
  });

  const filteredItems = useMemo(() => {
    const items = data?.items ?? [];
    if (!dateFilter) {
      return items;
    }
    return items.filter((item) =>
      item.completed_date.startsWith(dateFilter)
    );
  }, [data?.items, dateFilter]);

  const totalPages = data ? Math.max(1, Math.ceil(data.total / data.limit)) : 1;

  const updateParams = (next: Record<string, string>) => {
    const nextParams = new URLSearchParams(params);
    Object.entries(next).forEach(([key, value]) => {
      if (value) nextParams.set(key, value);
      else nextParams.delete(key);
    });
    nextParams.set("page", "1");
    setParams(nextParams);
  };

  if (isLoading) {
    return <div className="flex h-[70vh] items-center justify-center">Loading history...</div>;
  }

  if (error || !data) {
    return <div className="flex h-[70vh] items-center justify-center text-red-500">Failed to load history.</div>;
  }

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-4xl font-bold text-[#3D348B]">History</h1>
          <p className="mt-2 text-gray-500">
            Every completed practice session for the signed-in learner.
          </p>
        </div>
        <div className="text-sm text-gray-500">
          {data.total} total records
        </div>
      </div>

      <div className="grid gap-3 rounded-3xl bg-white p-4 shadow-sm lg:grid-cols-4">
        <label className="flex items-center gap-2 rounded-2xl bg-slate-50 px-4 py-3">
          <Search size={18} className="text-gray-400" />
          <input className="w-full bg-transparent outline-none" placeholder="Search history" value={search} onChange={(e) => setSearch(e.target.value)} onKeyDown={(e) => e.key === "Enter" && updateParams({ search })} />
        </label>
        <select className="rounded-2xl bg-slate-50 px-4 py-3" value={type} onChange={(e) => updateParams({ type: e.target.value })}>
          {practiceTypes.map((item) => <option key={item} value={item}>{item === "all" ? "All practice types" : item}</option>)}
        </select>
        <select className="rounded-2xl bg-slate-50 px-4 py-3" value={sort} onChange={(e) => updateParams({ sort: e.target.value })}>
          <option value="newest">Newest</option>
          <option value="oldest">Oldest</option>
          <option value="score_desc">Highest score</option>
          <option value="score_asc">Lowest score</option>
        </select>
        <label className="flex items-center gap-2 rounded-2xl bg-slate-50 px-4 py-3">
          <Filter size={18} className="text-gray-400" />
          <input type="date" className="w-full bg-transparent outline-none" value={dateFilter} onChange={(e) => setDateFilter(e.target.value)} />
        </label>
      </div>

      <section className="space-y-4">
        {filteredItems.length === 0 ? (
          <div className="rounded-3xl bg-white p-8 text-gray-500 shadow-sm">
            No practice history yet.
          </div>
        ) : (
          filteredItems.map((item) => (
            <article className="rounded-3xl bg-white p-6 shadow-sm" key={item.attempt_id}>
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div className="flex gap-3">
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-[#D0E6FF] text-[#3D348B]">
                    <HistoryIcon size={20} />
                  </div>
                  <div>
                    <h2 className="text-xl font-bold capitalize text-[#3D348B]">{item.practice_type.replaceAll("_", " ")}</h2>
                    <p className="text-sm text-gray-500">{item.title}</p>
                    <p className="text-sm text-gray-500">{new Date(item.completed_date).toLocaleString()}</p>
                  </div>
                </div>
                <div className="rounded-2xl bg-[#F5F6FC] px-5 py-3 text-center">
                  <p className="text-xs font-semibold text-gray-500">Score</p>
                  <p className="text-2xl font-bold text-[#3D348B]">{item.score ?? "N/A"}</p>
                </div>
              </div>
              <div className="mt-4 grid gap-3 md:grid-cols-4">
                <MiniMetric label="Difficulty" value={item.difficulty ?? "N/A"} />
                <MiniMetric label="Time Taken" value={item.duration != null ? `${item.duration} min` : "N/A"} />
                <MiniMetric label="Status" value={item.status} />
                <MiniMetric label="Feedback" value={item.feedback_summary ?? "N/A"} />
              </div>
              <div className="mt-4 flex justify-end">
                <Link className="rounded-full bg-[#3D348B] px-4 py-2 text-sm font-semibold text-white" to={`/history/${item.attempt_id}`}>
                  View Details
                </Link>
              </div>
            </article>
          ))
        )}
      </section>

      <div className="flex items-center justify-between">
        <button className="rounded-full border px-4 py-2 disabled:opacity-50" disabled={page <= 1} onClick={() => setParams({ ...Object.fromEntries(params.entries()), page: String(page - 1) })}>
          Previous
        </button>
        <span className="text-sm text-gray-500">Page {page} of {totalPages}</span>
        <button className="rounded-full border px-4 py-2 disabled:opacity-50" disabled={page >= totalPages} onClick={() => setParams({ ...Object.fromEntries(params.entries()), page: String(page + 1) })}>
          Next
        </button>
      </div>
    </div>
  );
}

function MiniMetric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl bg-[#F5F6FC] p-4">
      <p className="text-sm text-gray-500">{label}</p>
      <p className="mt-1 text-sm font-semibold text-[#3D348B]">{value}</p>
    </div>
  );
}
