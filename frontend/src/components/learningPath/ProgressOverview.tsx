import {
  TrendingUp,
  BookOpen,
  Target,
  Award,
} from "lucide-react";

interface ProgressOverviewProps {
  progress?: number;
  level?: string;
  completedLessons?: number;
  totalLessons?: number;
  focusSkill?: string;
}

export default function ProgressOverview({
  progress = 68,
  level = "Intermediate",
  completedLessons = 12,
  totalLessons = 20,
  focusSkill = "Vocabulary",
}: ProgressOverviewProps) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">

      {/* Header */}
      <div className="mb-8 flex items-center justify-between">

        <div>
          <h2 className="text-2xl font-bold text-[#3D348B]">
            Overall Progress
          </h2>

          <p className="mt-1 text-gray-500">
            Your learning journey so far
          </p>
        </div>

        <div className="rounded-2xl bg-gradient-to-r from-[#4CB1FF] to-[#3D348B] px-6 py-4 text-center text-white shadow-lg">
          <p className="text-sm opacity-90">
            Current Level
          </p>

          <h3 className="text-xl font-bold">
            {level}
          </h3>
        </div>

      </div>

      {/* Progress Circle */}
      <div className="mb-8 flex flex-col items-center">

        <div className="relative flex h-36 w-36 items-center justify-center rounded-full bg-gradient-to-br from-[#4CB1FF] to-[#3D348B] shadow-xl">

          <div className="flex h-28 w-28 items-center justify-center rounded-full bg-white">

            <div className="text-center">

              <h2 className="text-4xl font-bold text-[#3D348B]">
                {progress}%
              </h2>

              <p className="text-sm text-gray-500">
                Completed
              </p>

            </div>

          </div>

        </div>

        {/* Progress Bar */}
        <div className="mt-6 w-full">

          <div className="mb-2 flex justify-between text-sm">

            <span className="text-gray-500">
              Learning Progress
            </span>

            <span className="font-semibold text-[#3D348B]">
              {progress}%
            </span>

          </div>

          <div className="h-3 overflow-hidden rounded-full bg-slate-200">

            <div
              className="h-full rounded-full bg-gradient-to-r from-[#4CB1FF] to-[#3D348B]"
              style={{
                width: `${progress}%`,
              }}
            />

          </div>

        </div>

      </div>

      {/* Statistics */}
      <div className="grid grid-cols-2 gap-5">

        <div className="rounded-2xl bg-blue-50 p-5">

          <div className="mb-3 flex items-center gap-2 text-[#3D348B]">
            <BookOpen size={20} />
            <span className="font-semibold">
              Lessons
            </span>
          </div>

          <h3 className="text-3xl font-bold text-[#3D348B]">
            {completedLessons}
          </h3>

          <p className="text-gray-500">
            of {totalLessons} completed
          </p>

        </div>

        <div className="rounded-2xl bg-green-50 p-5">

          <div className="mb-3 flex items-center gap-2 text-green-700">
            <TrendingUp size={20} />
            <span className="font-semibold">
              Improvement
            </span>
          </div>

          <h3 className="text-3xl font-bold text-green-700">
            +12%
          </h3>

          <p className="text-gray-500">
            Since last week
          </p>

        </div>

        <div className="rounded-2xl bg-orange-50 p-5">

          <div className="mb-3 flex items-center gap-2 text-orange-600">
            <Target size={20} />
            <span className="font-semibold">
              Focus Skill
            </span>
          </div>

          <h3 className="text-xl font-bold text-orange-600">
            {focusSkill}
          </h3>

          <p className="text-gray-500">
            AI recommendation
          </p>

        </div>

        <div className="rounded-2xl bg-purple-50 p-5">

          <div className="mb-3 flex items-center gap-2 text-purple-700">
            <Award size={20} />
            <span className="font-semibold">
              Next Goal
            </span>
          </div>

          <h3 className="text-xl font-bold text-purple-700">
            80%
          </h3>

          <p className="text-gray-500">
            Reach Advanced Level
          </p>

        </div>

      </div>

    </div>
  );
}