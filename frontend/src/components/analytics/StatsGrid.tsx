interface StatsGridProps {
  grammar: number;
  vocabulary: number;
  fluency: number;
  pronunciation: number;
}

interface StatCardProps {
  title: string;
  value: number;
  color: string;
}

function StatCard({
  title,
  value,
  color,
}: StatCardProps) {
  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-lg">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-500">{title}</p>

          <h2 className="mt-2 text-4xl font-bold text-[#3D348B]">
            {value}%
          </h2>
        </div>

        <div
          className={`h-5 w-5 rounded-full ${color}`}
        />
      </div>

      <div className="mt-5 h-2 rounded-full bg-gray-200">
        <div
          className="h-2 rounded-full transition-all duration-700"
          style={{
            width: `${value}%`,
            backgroundColor:
              color === "bg-blue-500"
                ? "#3B82F6"
                : color === "bg-green-500"
                ? "#22C55E"
                : color === "bg-purple-500"
                ? "#8B5CF6"
                : "#F97316",
          }}
        />
      </div>
    </div>
  );
}

export default function StatsGrid({
  grammar,
  vocabulary,
  fluency,
  pronunciation,
}: StatsGridProps) {
  return (
    <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
      <StatCard
        title="Grammar"
        value={grammar}
        color="bg-blue-500"
      />

      <StatCard
        title="Vocabulary"
        value={vocabulary}
        color="bg-green-500"
      />

      <StatCard
        title="Fluency"
        value={fluency}
        color="bg-purple-500"
      />

      <StatCard
        title="Pronunciation"
        value={pronunciation}
        color="bg-orange-500"
      />
    </div>
  );
}