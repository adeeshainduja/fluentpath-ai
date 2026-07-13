import {
  AlertTriangle,
  ArrowRight,
} from "lucide-react";

const weakSkills = [
  {
    skill: "Grammar",
    score: 58,
    advice: "Practice Past Tense exercises.",
  },
  {
    skill: "Pronunciation",
    score: 63,
    advice: "Complete Speaking Challenge.",
  },
];

export default function WeakSkills() {
  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">
      <div className="flex items-center gap-3">
        <AlertTriangle
          size={24}
          className="text-orange-500"
        />

        <h2 className="text-xl font-bold text-[#3D348B]">
          AI Skill Analysis
        </h2>
      </div>

      <div className="mt-6 space-y-5">
        {weakSkills.map((item) => (
          <div
            key={item.skill}
            className="rounded-2xl border border-gray-200 p-5"
          >
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold">
                {item.skill}
              </h3>

              <span className="rounded-full bg-red-100 px-3 py-1 text-sm font-semibold text-red-600">
                {item.score}%
              </span>
            </div>

            <p className="mt-3 text-gray-500">
              {item.advice}
            </p>

            <button className="mt-4 flex items-center gap-2 font-semibold text-[#3D348B]">
              Practice Now

              <ArrowRight size={18} />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}