import {
  Award,
  Star,
  Trophy,
  Medal,
  Crown,
} from "lucide-react";

interface Badge {
  id: number;
  title: string;
  description: string;
  earned: boolean;
}

interface BadgeSectionProps {
  badges?: Badge[];
}

const defaultBadges: Badge[] = [
  {
    id: 1,
    title: "Grammar Master",
    description: "Achieved 90% in Grammar",
    earned: true,
  },
  {
    id: 2,
    title: "Vocabulary Explorer",
    description: "Learned 100 new words",
    earned: true,
  },
  {
    id: 3,
    title: "7 Day Streak",
    description: "Practiced for 7 consecutive days",
    earned: true,
  },
  {
    id: 4,
    title: "Speaking Champion",
    description: "Complete 20 speaking exercises",
    earned: false,
  },
  {
    id: 5,
    title: "Interview Ready",
    description: "Finish all interview practices",
    earned: false,
  },
];

const icons = [
  Award,
  Star,
  Trophy,
  Medal,
  Crown,
];

export default function BadgeSection({
  badges = defaultBadges,
}: BadgeSectionProps) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">

      <div className="mb-6">
        <h2 className="text-2xl font-bold text-[#3D348B]">
          Achievement Badges
        </h2>

        <p className="mt-1 text-sm text-gray-500">
          Unlock badges by completing learning milestones.
        </p>
      </div>

      <div className="space-y-4">

        {badges.map((badge, index) => {
          const Icon = icons[index % icons.length];

          return (
            <div
              key={badge.id}
              className={`flex items-center gap-4 rounded-2xl border p-4 transition-all duration-300 hover:shadow-md ${
                badge.earned
                  ? "border-blue-100 bg-gradient-to-r from-blue-50 to-indigo-50"
                  : "border-gray-200 bg-gray-50 opacity-70"
              }`}
            >
              <div
                className={`flex h-14 w-14 items-center justify-center rounded-2xl ${
                  badge.earned
                    ? "bg-gradient-to-br from-[#4CB1FF] to-[#3D348B] text-white"
                    : "bg-gray-300 text-white"
                }`}
              >
                <Icon size={26} />
              </div>

              <div className="flex-1">
                <h3 className="font-semibold text-[#3D348B]">
                  {badge.title}
                </h3>

                <p className="text-sm text-gray-500">
                  {badge.description}
                </p>
              </div>

              <div>
                {badge.earned ? (
                  <span className="rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700">
                    Earned
                  </span>
                ) : (
                  <span className="rounded-full bg-gray-200 px-3 py-1 text-xs font-semibold text-gray-600">
                    Locked
                  </span>
                )}
              </div>
            </div>
          );
        })}

      </div>
    </div>
  );
}