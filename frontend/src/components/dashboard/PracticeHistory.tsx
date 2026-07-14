import { Eye } from "lucide-react";
import { useNavigate } from "react-router-dom";

interface PracticeItem {
  task_id: number;
  target_skill: string;
  task_score: number;
  created_at: string;
}

interface PracticeHistoryProps {
  history: PracticeItem[];
}

export default function PracticeHistory({
  history,
}: PracticeHistoryProps) {

  const navigate = useNavigate();

  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">
      <h2 className="mb-6 text-xl font-bold text-[#3D348B]">
        Recent Practice
      </h2>

      <table className="w-full">
        <thead>
          <tr className="border-b text-left text-gray-500">
            <th className="pb-3">Date</th>
            <th className="pb-3">Skill</th>
            <th className="pb-3">Task ID</th>
            <th className="pb-3">Score</th>
            <th className="pb-3">Status</th>
            <th className="pb-3"></th>
          </tr>
        </thead>

        <tbody>
          {history.map((item) => (
            <tr
              key={item.task_id}
              className="border-b last:border-none"
            >
              <td className="py-4">
                {new Date(item.created_at).toLocaleDateString()}
              </td>

              <td>
                {item.target_skill
                  .replaceAll("_", " ")
                  .replace(/\b\w/g, (c) => c.toUpperCase())}
              </td>

              <td>#{item.task_id}</td>

              <td>{item.task_score}%</td>

              <td>
                <span className="font-medium text-green-600">
                  Completed
                </span>
              </td>

              <td>
                <button
                onClick={() => navigate(`/practice/${item.task_id}`)}
                className="rounded-lg p-2 hover:bg-gray-100"
              >
                <Eye size={18} />
              </button>
              </td>
            </tr>
          ))}

          {history.length === 0 && (
            <tr>
              <td
                colSpan={6}
                className="py-8 text-center text-gray-500"
              >
                No practice history found.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}