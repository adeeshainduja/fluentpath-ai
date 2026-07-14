import {
  BookOpen,
  Target,
  Clock,
  BarChart3,
  Play,
  ArrowRight,
} from "lucide-react";

interface Lesson {
  id: number;
  title: string;
  skill: string;
  difficulty: string;
  estimated_minutes: number;
}

interface CurrentLessonProps {
  lesson?: Lesson;
}

const defaultLesson: Lesson = {
  id: 1,
  title: "Business Email Writing",
  skill: "Vocabulary",
  difficulty: "Intermediate",
  estimated_minutes: 20,
};

export default function CurrentLesson({
  lesson = defaultLesson,
}: CurrentLessonProps) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">

      {/* Header */}
      <div className="mb-6 flex items-center gap-3">
        <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-[#4CB1FF] to-[#3D348B] text-white">
          <BookOpen size={28} />
        </div>

        <div>
          <h2 className="text-2xl font-bold text-[#3D348B]">
            Current Lesson
          </h2>

          <p className="text-sm text-gray-500">
            Continue your personalized learning journey
          </p>
        </div>
      </div>

      {/* Lesson Card */}
      <div className="rounded-2xl bg-gradient-to-r from-[#4CB1FF] to-[#3D348B] p-6 text-white">

        <p className="text-sm opacity-90">
          AI Recommended
        </p>

        <h3 className="mt-2 text-3xl font-bold">
          {lesson.title}
        </h3>

        <div className="mt-6 grid grid-cols-3 gap-4">

          <div className="rounded-xl bg-white/20 p-4">
            <Target size={20} />

            <p className="mt-2 text-sm opacity-80">
              Skill
            </p>

            <h4 className="font-semibold">
              {lesson.skill}
            </h4>
          </div>

          <div className="rounded-xl bg-white/20 p-4">
            <BarChart3 size={20} />

            <p className="mt-2 text-sm opacity-80">
              Difficulty
            </p>

            <h4 className="font-semibold">
              {lesson.difficulty}
            </h4>
          </div>

          <div className="rounded-xl bg-white/20 p-4">
            <Clock size={20} />

            <p className="mt-2 text-sm opacity-80">
              Duration
            </p>

            <h4 className="font-semibold">
              {lesson.estimated_minutes} min
            </h4>
          </div>

        </div>
      </div>

      {/* Progress */}
      <div className="mt-6">

        <div className="mb-2 flex justify-between text-sm">
          <span className="text-gray-600">
            Lesson Progress
          </span>

          <span className="font-semibold text-[#3D348B]">
            0%
          </span>
        </div>

        <div className="h-3 overflow-hidden rounded-full bg-slate-200">
          <div className="h-full w-0 rounded-full bg-gradient-to-r from-[#4CB1FF] to-[#3D348B]" />
        </div>

      </div>

      {/* Actions */}
      <div className="mt-8 flex gap-4">

        <button className="flex flex-1 items-center justify-center gap-2 rounded-2xl bg-[#3D348B] px-6 py-4 font-semibold text-white transition hover:bg-[#2d2668]">
          <Play size={20} />
          Start Lesson
        </button>

        <button className="flex items-center justify-center gap-2 rounded-2xl border border-[#3D348B] px-6 py-4 font-semibold text-[#3D348B] transition hover:bg-[#F5F6FC]">
          Details
          <ArrowRight size={18} />
        </button>

      </div>

    </div>
  );
}