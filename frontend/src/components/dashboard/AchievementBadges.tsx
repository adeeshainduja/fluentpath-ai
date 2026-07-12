import { Trophy } from "lucide-react";

export default function AchievementCard() {
  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">
      <div className="flex items-center gap-3">
        <Trophy className="text-yellow-500" />

        <h2 className="text-xl font-bold text-[#3D348B]">
          Achievements
        </h2>
      </div>

      <div className="mt-6 flex gap-4">

        <div className="rounded-xl bg-[#D0E6FF] p-4 text-center">
          🔥
          <p className="mt-2 text-sm">
            7 Day Streak
          </p>
        </div>

        <div className="rounded-xl bg-[#D0E6FF] p-4 text-center">
          🏆
          <p className="mt-2 text-sm">
            Grammar Master
          </p>
        </div>

        <div className="rounded-xl bg-[#D0E6FF] p-4 text-center">
          🚀
          <p className="mt-2 text-sm">
            Top Progress
          </p>
        </div>

      </div>
    </div>
  );
}