import {
  CheckCircle2,
  Compass,
  Flag,
  Route,
  Target,
  TrendingUp,
} from "lucide-react";
import { useLearningPath } from "../../hooks/useLearningPath";

const formatLabel = (value: string) =>
  value.replaceAll("_", " ");

export default function LearningPath() {
  const { data, isLoading, error } = useLearningPath();

  if (isLoading) {
    return (
      <div className="flex h-[70vh] items-center justify-center">
        <h1 className="text-xl font-semibold text-[#3D348B]">
          Loading learning path...
        </h1>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex h-[70vh] items-center justify-center">
        <h1 className="text-xl font-semibold text-red-500">
          Failed to load learning path.
        </h1>
      </div>
    );
  }

  const completed = data.tasks.filter((task) => task.completed);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-[#3D348B]">
          Learning Path
        </h1>
        <p className="text-gray-500">
          Adaptive goals generated from your practice history.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-4">
        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <p className="text-sm text-gray-500">Current Level</p>
          <h2 className="mt-2 text-3xl font-bold text-[#3D348B]">
            {data.current_level}
          </h2>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <p className="text-sm text-gray-500">Overall Progress</p>
          <h2 className="mt-2 text-3xl font-bold text-[#3D348B]">
            {data.overall_progress}%
          </h2>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <p className="text-sm text-gray-500">Current Goal</p>
          <h2 className="mt-2 text-2xl font-bold capitalize text-[#3D348B]">
            {formatLabel(data.current_focus)}
          </h2>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <p className="text-sm text-gray-500">Next Milestone</p>
          <h2 className="mt-2 text-2xl font-bold text-[#3D348B]">
            {data.next_milestone}
          </h2>
        </div>
      </div>

      <section className="rounded-2xl bg-white p-6 shadow-sm">
        <div className="flex items-center gap-3">
          <Compass className="text-[#3D348B]" size={24} />
          <h2 className="text-xl font-bold text-[#3D348B]">
            Recommended Practice
          </h2>
        </div>

        <div className="mt-5 rounded-xl border border-gray-100 bg-[#F5F6FC] p-5">
          <p className="font-semibold capitalize text-[#3D348B]">
            {formatLabel(data.recommended_practice)}
          </p>
          <p className="mt-2 text-gray-600">{data.today_recommendation}</p>
          <p className="mt-3 text-sm text-gray-500">
            Focus on the weakest skill to keep the roadmap adaptive.
          </p>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-8 xl:grid-cols-3">
        <div className="xl:col-span-2 rounded-2xl bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <Target className="text-[#3D348B]" size={24} />
            <h2 className="text-xl font-bold text-[#3D348B]">
              Adaptive Goals
            </h2>
          </div>

          <div className="mt-5 space-y-4">
            {data.tasks.map((task) => (
              <div
                key={task.title}
                className="rounded-xl border border-gray-100 p-5"
              >
                <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                  <div>
                    <h3 className="font-semibold text-[#4A4B4B]">
                      {task.title}
                    </h3>
                    <p className="mt-1 text-sm text-gray-500">
                      {task.completed ? "Completed" : "Pending"}
                    </p>
                  </div>
                  <span className="rounded-full bg-[#D0E6FF] px-4 py-2 text-sm font-semibold text-[#3D348B]">
                    {task.completed ? "Done" : "Open"}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="space-y-8">
          <div className="rounded-2xl bg-white p-6 shadow-sm">
            <div className="flex items-center gap-3">
              <CheckCircle2 className="text-[#3D348B]" size={22} />
              <h2 className="text-lg font-bold text-[#3D348B]">
                Completed Skills
              </h2>
            </div>
            <div className="mt-4 space-y-3">
              {data.completed_tasks.length > 0 ? data.completed_tasks.map((task) => (
                <div
                  key={task.title}
                  className="rounded-lg bg-[#F5F6FC] px-4 py-3 text-sm font-medium capitalize text-[#4A4B4B]"
                >
                  {task.title}
                </div>
              )) : (
                <p className="text-sm text-gray-500">
                  No completed skills have been identified yet.
                </p>
              )}
            </div>
          </div>

          <div className="rounded-2xl bg-white p-6 shadow-sm">
            <div className="flex items-center gap-3">
              <Flag className="text-[#3D348B]" size={22} />
              <h2 className="text-lg font-bold text-[#3D348B]">
                Remaining Skills
              </h2>
            </div>
            <div className="mt-4 space-y-3">
              {data.weak_skills.map((skill) => (
                <div
                  key={skill}
                  className="rounded-lg bg-[#F5F6FC] px-4 py-3 text-sm font-medium capitalize text-[#4A4B4B]"
                >
                  {skill}
                </div>
              ))}
              {data.weak_skills.length === 0 && (
                <p className="text-sm text-gray-500">
                  No remaining priority skills are available.
                </p>
              )}
            </div>
          </div>
        </div>
      </section>

      <section className="rounded-2xl bg-white p-6 shadow-sm">
        <div className="flex items-center gap-3">
          <Route className="text-[#3D348B]" size={24} />
          <h2 className="text-xl font-bold text-[#3D348B]">
            Progress Timeline
          </h2>
        </div>

        <div className="mt-5 grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
          {path.goals.map((goal, index) => (
            <div
              key={`${goal.goal}-${index}`}
              className="rounded-xl border border-gray-100 p-5"
            >
              <p className="text-sm font-semibold text-[#3D348B]">
              {item.date}
            </p>
              <h3 className="mt-2 font-semibold text-[#4A4B4B]">{item.score}</h3>
              <p className="mt-2 text-sm capitalize text-gray-500">
                Score trend
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="rounded-2xl bg-white p-6 shadow-sm">
        <div className="flex items-center gap-3">
          <TrendingUp className="text-[#3D348B]" size={24} />
          <h2 className="text-xl font-bold text-[#3D348B]">
            Progress Bar
          </h2>
        </div>
        <div className="mt-5 h-4 rounded-full bg-gray-100">
          <div
            className="h-4 rounded-full bg-gradient-to-r from-[#3D348B] to-[#4CB1FF]"
            style={{ width: `${data.progress_bar}%` }}
          />
        </div>
      </section>
    </div>
  );
}
