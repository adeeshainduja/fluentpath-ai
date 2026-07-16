import {
  CheckCircle2,
  Compass,
  Flag,
  Route,
  Target,
} from "lucide-react";
import { useLearnerIntelligence } from "../../hooks/useLearnerIntelligence";

const learnerId = 1;

const formatLabel = (value: string | null) =>
  value ? value.replaceAll("_", " ") : "No data";

export default function LearningPath() {
  const { data, isLoading, error } =
    useLearnerIntelligence(learnerId);

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

  const path = data.learning_path;

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
            {path.current_level}
          </h2>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <p className="text-sm text-gray-500">Current Focus</p>
          <h2 className="mt-2 text-2xl font-bold capitalize text-[#3D348B]">
            {formatLabel(path.current_focus)}
          </h2>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <p className="text-sm text-gray-500">Progress</p>
          <h2 className="mt-2 text-3xl font-bold text-[#3D348B]">
            {path.progress ?? "No data"}
          </h2>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <p className="text-sm text-gray-500">Active Goals</p>
          <h2 className="mt-2 text-3xl font-bold text-[#3D348B]">
            {path.goals.length}
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

        {path.recommended_practice ? (
          <div className="mt-5 rounded-xl border border-gray-100 bg-[#F5F6FC] p-5">
            <p className="font-semibold capitalize text-[#3D348B]">
              {formatLabel(
                path.recommended_practice.affected_skill
              )}
            </p>
            <p className="mt-2 text-gray-600">
              {path.recommended_practice.recommendation}
            </p>
            <p className="mt-3 text-sm text-gray-500">
              {path.recommended_practice.reason}
            </p>
          </div>
        ) : (
          <p className="mt-5 text-gray-500">
            No recommendation is available from the current learner
            data.
          </p>
        )}
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
            {path.goals.map((goal) => (
              <div
                key={`${goal.target_skill}-${goal.priority}`}
                className="rounded-xl border border-gray-100 p-5"
              >
                <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                  <div>
                    <h3 className="font-semibold text-[#4A4B4B]">
                      {goal.goal}
                    </h3>
                    <p className="mt-1 text-sm text-gray-500">
                      {goal.reason}
                    </p>
                  </div>
                  <span className="rounded-full bg-[#D0E6FF] px-4 py-2 text-sm font-semibold text-[#3D348B]">
                    Priority {goal.priority}
                  </span>
                </div>
                <p className="mt-3 text-sm text-gray-500">
                  {goal.success_metric}
                </p>
              </div>
            ))}

            {path.goals.length === 0 && (
              <p className="text-gray-500">
                No adaptive goals are available yet.
              </p>
            )}
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
              {path.completed_skills.map((skill) => (
                <div
                  key={skill}
                  className="rounded-lg bg-[#F5F6FC] px-4 py-3 text-sm font-medium capitalize text-[#4A4B4B]"
                >
                  {formatLabel(skill)}
                </div>
              ))}
              {path.completed_skills.length === 0 && (
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
              {path.remaining_skills.map((skill) => (
                <div
                  key={skill}
                  className="rounded-lg bg-[#F5F6FC] px-4 py-3 text-sm font-medium capitalize text-[#4A4B4B]"
                >
                  {formatLabel(skill)}
                </div>
              ))}
              {path.remaining_skills.length === 0 && (
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
                Step {index + 1}
              </p>
              <h3 className="mt-2 font-semibold text-[#4A4B4B]">
                {goal.goal}
              </h3>
              <p className="mt-2 text-sm capitalize text-gray-500">
                {formatLabel(goal.suggested_practice_type)}
              </p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
