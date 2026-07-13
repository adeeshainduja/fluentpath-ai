import { Award, Flame, Star } from "lucide-react";

const badges = [
  {
    title: "7 Day Streak",
    icon: Flame,
    color: "text-orange-500",
  },
  {
    title: "Grammar Master",
    icon: Award,
    color: "text-blue-500",
  },
  {
    title: "Top Performer",
    icon: Star,
    color: "text-yellow-500",
  },
];

export default function AchievementBadges() {
  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">
      <h2 className="text-xl font-bold text-[#3D348B]">
        Achievements
      </h2>

      <div className="mt-6 grid grid-cols-3 gap-4">

        {badges.map((badge) => {
          const Icon = badge.icon;

          return (
            <div
              key={badge.title}
              className="rounded-2xl border p-5 text-center hover:shadow-md"
            >
              <Icon
                size={40}
                className={`mx-auto ${badge.color}`}
              />

              <p className="mt-3 text-sm font-semibold">
                {badge.title}
              </p>
            </div>
          );
        })}

      </div>
    </div>
  );
}