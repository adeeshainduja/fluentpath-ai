import {
  PolarAngleAxis,
  PolarGrid,
  Radar,
  RadarChart,
  ResponsiveContainer,
} from "recharts";

interface SkillProgress {
  skill: string;
  average_score: number;
}

interface SkillRadarProps {
  skills: SkillProgress[];
}

export default function SkillRadar({
  skills,
}: SkillRadarProps) {
  const radarData = skills.map((item) => ({
    skill: item.skill
      .replaceAll("_", " ")
      .replace(/\b\w/g, (c) => c.toUpperCase()),
    score: item.average_score,
  }));

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
        <RadarChart data={radarData}>
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