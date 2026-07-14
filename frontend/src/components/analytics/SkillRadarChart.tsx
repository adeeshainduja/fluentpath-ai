import {
  PolarAngleAxis,
  PolarGrid,
  Radar,
  RadarChart,
  ResponsiveContainer,
} from "recharts";

interface Props {
  grammar: number;
  vocabulary: number;
  fluency: number;
  pronunciation: number;
}

export default function SkillRadarChart({
  grammar,
  vocabulary,
  fluency,
  pronunciation,
}: Props) {
  const data = [
    {
      skill: "Grammar",
      score: grammar,
    },
    {
      skill: "Vocabulary",
      score: vocabulary,
    },
    {
      skill: "Fluency",
      score: fluency,
    },
    {
      skill: "Pronunciation",
      score: pronunciation,
    },
  ];

  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-[#3D348B]">
          Skill Performance
        </h2>

        <p className="text-gray-500">
          Performance across English skills.
        </p>
      </div>

      <ResponsiveContainer
        width="100%"
        height={340}
      >
        <RadarChart data={data}>
          <PolarGrid />

          <PolarAngleAxis dataKey="skill" />

          <Radar
            dataKey="score"
            stroke="#3D348B"
            fill="#4CB1FF"
            fillOpacity={0.6}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}