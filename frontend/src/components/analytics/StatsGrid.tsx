interface StatsGridProps {
  grammar: number;
  vocabulary: number;
  fluency: number;
  pronunciation: number;
}

const stats = [
  {
    key: "grammar",
    label: "Grammar",
    color: "bg-blue-500",
  },
  {
    key: "vocabulary",
    label: "Vocabulary",
    color: "bg-green-500",
  },
  {
    key: "fluency",
    label: "Fluency",
    color: "bg-purple-500",
  },
  {
    key: "pronunciation",
    label: "Pronunciation",
    color: "bg-orange-500",
  },
];

export default function StatsGrid({
  grammar,
  vocabulary,
  fluency,
  pronunciation,
}: StatsGridProps) {
  const values = {
    grammar,
    vocabulary,
    fluency,
    pronunciation,
  };

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">
      {stats.map((item) => (
        <div
          key={item.key}
          className="rounded-3xl bg-white p-6 shadow-sm"
        >
          <div
            className={`mb-4 h-3 w-16 rounded-full ${item.color}`}
          />

          <p className="text-gray-500">
            {item.label}
          </p>

          <h2 className="mt-2 text-3xl font-bold text-[#3D348B]">
            {values[item.key as keyof typeof values]}%
          </h2>
        </div>
      ))}
    </div>
  );
}