import {
  Flame,
  CalendarDays,
  Trophy,
  TrendingUp,
} from "lucide-react";

interface StreakCardProps {
  streak?: number;
  longestStreak?: number;
  todayCompleted?: boolean;
}

export default function StreakCard({
  streak = 5,
  longestStreak = 12,
  todayCompleted = true,
}: StreakCardProps) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">

      {/* Header */}
      <div className="mb-6 flex items-center gap-4">

        <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-orange-400 to-red-500 text-white shadow-lg">
          <Flame size={28} />
        </div>

        <div>
          <h2 className="text-2xl font-bold text-[#3D348B]">
            Learning Streak
          </h2>

          <p className="text-sm text-gray-500">
            Stay consistent every day
          </p>
        </div>

      </div>

      {/* Current Streak */}
      <div className="rounded-2xl bg-gradient-to-r from-orange-400 to-red-500 p-6 text-center text-white">

        <p className="text-sm opacity-90">
          Current Streak
        </p>

        <h1 className="mt-2 text-5xl font-bold">
          {streak}
        </h1>

        <p className="mt-1 text-lg">
          Days 🔥
        </p>

      </div>

      {/* Statistics */}
      <div className="mt-6 grid grid-cols-2 gap-4">

        <div className="rounded-2xl bg-blue-50 p-4 text-center">

          <CalendarDays
            className="mx-auto mb-2 text-[#3D348B]"
            size={22}
          />

          <p className="text-sm text-gray-500">
            Today
          </p>

          <h3
            className={`mt-1 font-bold ${
              todayCompleted
                ? "text-green-600"
                : "text-red-500"
            }`}
          >
            {todayCompleted
              ? "Completed"
              : "Pending"}
          </h3>

        </div>

        <div className="rounded-2xl bg-purple-50 p-4 text-center">

          <Trophy
            className="mx-auto mb-2 text-purple-600"
            size={22}
          />

          <p className="text-sm text-gray-500">
            Best
          </p>

          <h3 className="mt-1 text-xl font-bold text-purple-700">
            {longestStreak} Days
          </h3>

        </div>

      </div>

      {/* Weekly Progress */}
      <div className="mt-6">

        <div className="mb-3 flex items-center gap-2">

          <TrendingUp
            className="text-[#3D348B]"
            size={20}
          />

          <h3 className="font-semibold text-[#3D348B]">
            This Week
          </h3>

        </div>

        <div className="flex justify-between">

          {[
            "M",
            "T",
            "W",
            "T",
            "F",
            "S",
            "S",
          ].map((day, index) => (
            <div
              key={index}
              className={`flex h-11 w-11 items-center justify-center rounded-full font-semibold ${
                index < 5
                  ? "bg-gradient-to-br from-[#4CB1FF] to-[#3D348B] text-white"
                  : "bg-slate-200 text-gray-500"
              }`}
            >
              {day}
            </div>
          ))}

        </div>

      </div>

      {/* Motivation */}
      <div className="mt-6 rounded-2xl bg-[#F5F6FC] p-4">

        <p className="text-center text-sm text-gray-600">
          🎯 Keep practicing tomorrow to extend your streak and
          unlock new achievement badges!
        </p>

      </div>

    </div>
  );
}