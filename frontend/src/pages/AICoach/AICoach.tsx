import {
  AlertTriangle,
  BarChart3,
  CheckCircle2,
  Lightbulb,
  Sparkles,
} from "lucide-react";
import { useLearnerIntelligence } from "../../hooks/useLearnerIntelligence";

const learnerId = 1;

const formatLabel = (value: string) =>
  value.replaceAll("_", " ");

export default function AICoach() {
  const { data, isLoading, error } =
    useLearnerIntelligence(learnerId);

  if (isLoading) {
    return (
      <div className="flex h-[70vh] items-center justify-center">
        <h1 className="text-xl font-semibold text-[#3D348B]">
          Loading AI coach...
        </h1>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex h-[70vh] items-center justify-center">
        <h1 className="text-xl font-semibold text-red-500">
          Failed to load AI coach.
        </h1>
      </div>
    );
  }

  const weaknesses = [
    ...data.weaknesses.grammar_topics,
    ...data.weaknesses.vocabulary_weaknesses,
    ...data.weaknesses.pronunciation_weaknesses,
    ...data.weaknesses.fluency_weaknesses,
    ...data.weaknesses.confidence_weaknesses,
  ];

  const strengths = [
    ...data.strengths.highest_performing_skills,
    ...data.strengths.most_improved_skills,
    ...data.strengths.consistent_strengths,
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-[#3D348B]">
          AI Coach
        </h1>
        <p className="text-gray-500">
          Explainable coaching insights from your learner data.
        </p>
      </div>

      <section className="rounded-2xl bg-gradient-to-br from-[#3D348B] to-[#4CB1FF] p-8 text-white shadow-lg">
        <div className="flex items-center gap-3">
          <Sparkles size={28} />
          <h2 className="text-xl font-bold">Coach Insight</h2>
        </div>
        <p className="mt-5 max-w-4xl leading-7 text-white/90">
          {data.dashboard_insights.ai_insight}
        </p>
      </section>

      <section className="grid grid-cols-1 gap-6 xl:grid-cols-4">
        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <p className="text-sm text-gray-500">Current Level</p>
          <h2 className="mt-2 text-3xl font-bold text-[#3D348B]">
            {data.dashboard_insights.current_level}
          </h2>
        </div>
        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <p className="text-sm text-gray-500">Focus</p>
          <h2 className="mt-2 text-2xl font-bold capitalize text-[#3D348B]">
            {data.dashboard_insights.current_focus
              ? formatLabel(data.dashboard_insights.current_focus)
              : "No data"}
          </h2>
        </div>
        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <p className="text-sm text-gray-500">Consistency</p>
          <h2 className="mt-2 text-2xl font-bold capitalize text-[#3D348B]">
            {formatLabel(data.performance.consistency_label)}
          </h2>
        </div>
        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <p className="text-sm text-gray-500">Streak</p>
          <h2 className="mt-2 text-3xl font-bold text-[#3D348B]">
            {data.dashboard_insights.practice_streak}
          </h2>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-8 xl:grid-cols-3">
        <div className="xl:col-span-2 rounded-2xl bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <Lightbulb className="text-[#3D348B]" size={24} />
            <h2 className="text-xl font-bold text-[#3D348B]">
              Explainable Recommendations
            </h2>
          </div>

          <div className="mt-5 space-y-4">
            {data.recommendations.recommendations.map(
              (recommendation) => (
                <div
                  key={`${recommendation.affected_skill}-${recommendation.priority}`}
                  className="rounded-xl border border-gray-100 p-5"
                >
                  <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                    <div>
                      <h3 className="font-semibold text-[#4A4B4B]">
                        {recommendation.recommendation}
                      </h3>
                      <p className="mt-2 text-sm text-gray-500">
                        {recommendation.reason}
                      </p>
                    </div>
                    <span className="rounded-full bg-[#D0E6FF] px-4 py-2 text-sm font-semibold text-[#3D348B]">
                      Priority {recommendation.priority}
                    </span>
                  </div>
                  <div className="mt-4 grid grid-cols-1 gap-3 text-sm md:grid-cols-3">
                    <p className="capitalize text-gray-500">
                      Skill:{" "}
                      <span className="font-semibold text-[#4A4B4B]">
                        {formatLabel(recommendation.affected_skill)}
                      </span>
                    </p>
                    <p className="capitalize text-gray-500">
                      Practice:{" "}
                      <span className="font-semibold text-[#4A4B4B]">
                        {formatLabel(
                          recommendation.suggested_practice_type
                        )}
                      </span>
                    </p>
                    <p className="text-gray-500">
                      Confidence:{" "}
                      <span className="font-semibold text-[#4A4B4B]">
                        {Math.round(
                          recommendation.confidence * 100
                        )}
                        %
                      </span>
                    </p>
                  </div>
                </div>
              )
            )}

            {data.recommendations.recommendations.length === 0 && (
              <p className="text-gray-500">
                No data-backed recommendations are available yet.
              </p>
            )}
          </div>
        </div>

        <div className="space-y-8">
          <div className="rounded-2xl bg-white p-6 shadow-sm">
            <div className="flex items-center gap-3">
              <BarChart3 className="text-[#3D348B]" size={22} />
              <h2 className="text-lg font-bold text-[#3D348B]">
                Performance Summary
              </h2>
            </div>
            <div className="mt-4 space-y-3">
              {data.performance.average_scores_by_skill
                .slice(0, 5)
                .map((skill) => (
                  <div
                    key={skill.skill}
                    className="flex items-center justify-between rounded-lg bg-[#F5F6FC] px-4 py-3"
                  >
                    <span className="capitalize text-[#4A4B4B]">
                      {formatLabel(skill.skill)}
                    </span>
                    <span className="font-semibold text-[#3D348B]">
                      {skill.average_score}
                    </span>
                  </div>
                ))}
            </div>
          </div>

          <div className="rounded-2xl bg-white p-6 shadow-sm">
            <div className="flex items-center gap-3">
              <CheckCircle2 className="text-[#3D348B]" size={22} />
              <h2 className="text-lg font-bold text-[#3D348B]">
                Strengths
              </h2>
            </div>
            <div className="mt-4 space-y-3">
              {strengths.slice(0, 4).map((strength) => (
                <p
                  key={`${strength.category}-${strength.skill}`}
                  className="rounded-lg bg-[#F5F6FC] px-4 py-3 text-sm text-gray-600"
                >
                  <span className="font-semibold capitalize text-[#4A4B4B]">
                    {formatLabel(strength.skill)}
                  </span>{" "}
                  {strength.evidence}
                </p>
              ))}
              {strengths.length === 0 && (
                <p className="text-sm text-gray-500">
                  No strengths have been identified yet.
                </p>
              )}
            </div>
          </div>

          <div className="rounded-2xl bg-white p-6 shadow-sm">
            <div className="flex items-center gap-3">
              <AlertTriangle className="text-[#3D348B]" size={22} />
              <h2 className="text-lg font-bold text-[#3D348B]">
                Weaknesses
              </h2>
            </div>
            <div className="mt-4 space-y-3">
              {weaknesses.slice(0, 4).map((weakness) => (
                <p
                  key={`${weakness.category}-${weakness.skill}`}
                  className="rounded-lg bg-[#F5F6FC] px-4 py-3 text-sm text-gray-600"
                >
                  <span className="font-semibold capitalize text-[#4A4B4B]">
                    {formatLabel(weakness.skill)}
                  </span>{" "}
                  {weakness.evidence}
                </p>
              ))}
              {weaknesses.length === 0 && (
                <p className="text-sm text-gray-500">
                  No weaknesses have been identified yet.
                </p>
              )}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
