import {
  PolarAngleAxis,
  PolarGrid,
  Radar,
  RadarChart,
  ResponsiveContainer,
} from "recharts";

const data = [
  { skill: "Grammar", score: 78 },
  { skill: "Vocabulary", score: 90 },
  { skill: "Pronunciation", score: 70 },
  { skill: "Fluency", score: 82 },
  { skill: "Listening", score: 75 },
  { skill: "Writing", score: 88 },
];

export default function SkillRadar() {
  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">
      <div className="mb-6">
        <h2 className="text-xl font-bold text-[#3D348B]">
          Skill Overview
        </h2>

        <p className="text-sm text-gray-500">
          Performance by English skill
        </p>
      </div>

      <ResponsiveContainer width="100%" height={320}>
        <RadarChart data={data}>
          <PolarGrid />

          <PolarAngleAxis dataKey="skill" />

          <Radar
            dataKey="score"
            stroke="#3D348B"
            fill="#4CB1FF"
            fillOpacity={0.55}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}