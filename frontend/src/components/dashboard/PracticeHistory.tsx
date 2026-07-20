import { Eye } from "lucide-react";
import { useNavigate } from "react-router-dom";
import type { DashboardPracticeItem } from "../../types/dashboard";

interface PracticeHistoryProps {
  latestPractice: DashboardPracticeItem | null;
}

export default function PracticeHistory({
  latestPractice,
}: PracticeHistoryProps) {
  const navigate = useNavigate();

  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">
      <h2 className="mb-6 text-xl font-bold text-[#3D348B]">
        Latest Practice
      </h2>

      {!latestPractice ? (
        <p className="text-gray-500">
          No completed practice yet.
        </p>
      ) : (
        <div className="flex flex-wrap items-center justify-between gap-4 rounded-2xl border border-gray-200 p-5">
          <div>
            <p className="text-sm text-gray-500">
              {new Date(latestPractice.created_at).toLocaleDateString()}
            </p>
            <h3 className="mt-2 text-lg font-semibold text-[#3D348B]">
              {latestPractice.title ?? "Practice"}
            </h3>
            <p className="mt-1 text-gray-600">
              {latestPractice.target_skill ?? "Unknown skill"}
              {latestPractice.score !== null && latestPractice.score !== undefined
                ? ` · ${latestPractice.score}%`
                : ""}
            </p>
          </div>

          {latestPractice.task_id ? (
            <button
              type="button"
              onClick={() => navigate(`/practice/${latestPractice.task_id}`)}
              className="rounded-lg p-2 hover:bg-gray-100"
            >
              <Eye size={18} />
            </button>
          ) : null}
        </div>
      )}
    </div>
  );
}
