interface PracticeHistoryItem {
  date: string;
  skill: string;
  score: number;
  status: string;
}

interface PracticeHistoryTableProps {
  history: PracticeHistoryItem[];
}

export default function PracticeHistoryTable({
  history,
}: PracticeHistoryTableProps) {
  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-[#3D348B]">
          Recent Practice
        </h2>

        <p className="text-gray-500">
          Your latest completed activities.
        </p>
      </div>

      <table className="w-full">
        <thead>
          <tr className="border-b text-left">
            <th className="pb-3">Date</th>
            <th className="pb-3">Skill</th>
            <th className="pb-3">Score</th>
            <th className="pb-3">Status</th>
          </tr>
        </thead>

        <tbody>
          {history.map((item, index) => (
            <tr
              key={index}
              className="border-b last:border-none"
            >
              <td className="py-4">
                {item.date}
              </td>

              <td>{item.skill}</td>

              <td>{item.score}%</td>

              <td>
                <span className="rounded-full bg-green-100 px-3 py-1 text-sm text-green-600">
                  {item.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}