interface Props {
  grammar: number;
  vocabulary: number;
  fluency: number;
  pronunciation: number;
}

function SkillCard({
  title,
  score,
  color,
}: {
  title: string;
  score: number;
  color: string;
}) {
  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">

      <div className="flex items-center justify-between">

        <div>

          <p className="text-gray-500">
            {title}
          </p>

          <h2 className="mt-2 text-4xl font-bold text-[#3D348B]">
            {score}%
          </h2>

        </div>

        <div
          className={`h-5 w-5 rounded-full ${color}`}
        />

      </div>

      <div className="mt-5 h-2 rounded-full bg-gray-200">

        <div
          className="h-2 rounded-full"
          style={{
            width: `${score}%`,
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
}: Props) {
  return (
    <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">

      <SkillCard
        title="Grammar"
        score={grammar}
        color="bg-blue-500"
      />

      <SkillCard
        title="Vocabulary"
        score={vocabulary}
        color="bg-green-500"
      />

      <SkillCard
        title="Fluency"
        score={fluency}
        color="bg-purple-500"
      />

      <SkillCard
        title="Pronunciation"
        score={pronunciation}
        color="bg-orange-500"
      />

    </div>
  );
}