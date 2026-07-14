import { Award, BookOpen, Flame } from "lucide-react";
import type { AchievementBadge } from "../../types/dashboard";

interface Props {
  badges: AchievementBadge[];
}

const icons = {
  award: Award,
  flame: Flame,
  book: BookOpen,
};

export default function AchievementBadges({ badges }: Props) {
  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">
      <h2 className="mb-6 text-xl font-bold text-[#3D348B]">
        Achievements
      </h2>

      <div className="space-y-4">
        {badges.map((badge) => {
          const Icon =
            icons[badge.icon as keyof typeof icons] ?? Award;

          return (
            <div
              key={badge.title}
              className={`flex items-center gap-4 rounded-xl border p-4 ${
                badge.earned
                  ? "border-green-200 bg-green-50"
                  : "border-gray-200"
              }`}
            >
              <Icon
                className={
                  badge.earned
                    ? "text-green-600"
                    : "text-gray-400"
                }
                size={24}
              />

              <div>
                <h3 className="font-semibold">{badge.title}</h3>

                <p className="text-sm text-gray-500">
                  {badge.description}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}