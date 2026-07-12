import { Eye } from "lucide-react";

const history = [
  {
    date: "12 Jul",
    skill: "Grammar",
    type: "Writing",
    score: 86,
    status: "Completed",
  },
  {
    date: "11 Jul",
    skill: "Vocabulary",
    type: "Speaking",
    score: 91,
    status: "Completed",
  },
  {
    date: "10 Jul",
    skill: "Fluency",
    type: "Speaking",
    score: 79,
    status: "Completed",
  },
];

export default function PracticeHistory() {
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
            <th className="pb-3">Type</th>
            <th className="pb-3">Score</th>
            <th className="pb-3">Status</th>
            <th className="pb-3"></th>
          </tr>
        </thead>

        <tbody>
          {history.map((item, index) => (
            <tr
              key={index}
              className="border-b last:border-none"
            >
              <td className="py-4">{item.date}</td>
              <td>{item.skill}</td>
              <td>{item.type}</td>
              <td>{item.score}%</td>
              <td className="text-green-600">{item.status}</td>
              <td>
                <button className="rounded-lg p-2 hover:bg-gray-100">
                  <Eye size={18} />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}