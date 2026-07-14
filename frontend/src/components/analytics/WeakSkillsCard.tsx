interface WeakSkill {
  skill: string;
  score: number;
  recommendation: string;
  priority: string;
}

interface WeakSkillsCardProps {
  skills: WeakSkill[];
}

export default function WeakSkillsCard({
  skills,
}: WeakSkillsCardProps) {
  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">
      <h2 className="mb-6 text-2xl font-bold text-[#3D348B]">
        Weak Skills
      </h2>

      <div className="space-y-5">
        {skills.map((skill) => (
          <div
            key={skill.skill}
            className="rounded-2xl border border-gray-200 p-5 transition hover:shadow-md"
          >
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold">
                {skill.skill}
              </h3>

              <span className="rounded-full bg-red-100 px-3 py-1 text-sm font-semibold text-red-600">
                {skill.score}%
              </span>
            </div>

            <p className="mt-3 text-gray-500">
              {skill.recommendation}
            </p>

            <span className="mt-4 inline-block rounded-full bg-orange-100 px-3 py-1 text-xs font-semibold text-orange-700">
              {skill.priority} Priority
            </span>

            <button className="mt-5 rounded-xl bg-[#3D348B] px-5 py-2 text-white transition hover:bg-[#2E276A]">
              Practice Now
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}