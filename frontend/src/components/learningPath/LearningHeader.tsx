import { Sparkles, Flame } from "lucide-react";

interface LearningHeaderProps {
  streak?: number;
}

export default function LearningHeader({
  streak = 5,
}: LearningHeaderProps) {
  return (
    <div className="flex items-center justify-between rounded-3xl bg-white p-8 shadow-sm border border-slate-200">

      {/* Left */}
      <div>
        <div className="mb-3 flex items-center gap-2">
          <Sparkles
            className="text-[#4CB1FF]"
            size={28}
          />

          <h1 className="text-4xl font-bold text-[#3D348B]">
            Personalized Learning Path
          </h1>
        </div>

        <p className="max-w-2xl text-gray-500">
          Your AI-generated roadmap continuously adapts to your
          strengths, weaknesses, and learning progress. Complete
          lessons to unlock new challenges and improve your English
          skills.
        </p>
      </div>

      {/* Right */}
      <div className="flex items-center gap-3 rounded-2xl bg-gradient-to-r from-orange-400 to-red-500 px-6 py-4 text-white shadow-lg">

        <Flame size={30} />

        <div>
          <p className="text-sm opacity-90">
            Current Streak
          </p>

          <h2 className="text-2xl font-bold">
            {streak} Days 🔥
          </h2>
        </div>

      </div>
    </div>
  );
}