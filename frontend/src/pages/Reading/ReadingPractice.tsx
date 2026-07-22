import { useEffect, useMemo, useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { CheckCircle2, Clock3, BookOpenText } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../../hooks/useAuth";
import {
  generateReadingPractice,
  submitReadingPractice,
} from "../../services/readingApi";
import type {
  ReadingSubmissionResponse,
  ReadingPractice,
} from "../../types/reading";

type AnswerMap = Record<number, string>;

export default function ReadingPractice() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [answers, setAnswers] = useState<AnswerMap>({});
  const [result, setResult] =
    useState<ReadingSubmissionResponse | null>(null);
  const [message, setMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { data, isLoading, error } = useQuery<ReadingPractice>({
    queryKey: ["reading-practice", user?.id ?? "me"],
    queryFn: generateReadingPractice,
    enabled: Boolean(user),
  });

  useEffect(() => {
    if (!user) {
      navigate("/login");
    }
  }, [navigate, user]);

  useEffect(() => {
    if (data) {
      setAnswers(
        Object.fromEntries(
          data.questions.map((question) => [question.id, ""])
        )
      );
      setResult(null);
      setMessage("");
    }
  }, [data]);

  const allAnswered = useMemo(
    () =>
      data?.questions.every((question) =>
        Boolean(answers[question.id])
      ) ?? false,
    [answers, data]
  );

  const handleSelect = (questionId: number, value: string) => {
    setAnswers((current) => ({
      ...current,
      [questionId]: value,
    }));
  };

  const handleSubmit = async () => {
    if (!data) {
      return;
    }

    if (!allAnswered) {
      setMessage("Please answer all 5 questions before submitting.");
      return;
    }

    setIsSubmitting(true);
    setMessage("");

    try {
      const submission = await submitReadingPractice({
        learner_id: user?.id,
        passage_id: data.passage_id,
        answers,
      });

      setResult(submission);

      await Promise.all([
        queryClient.invalidateQueries({
          queryKey: ["dashboard"],
        }),
        queryClient.invalidateQueries({
          queryKey: ["history"],
        }),
        queryClient.invalidateQueries({
          queryKey: ["analytics"],
        }),
        queryClient.invalidateQueries({
          queryKey: ["learning-path"],
        }),
      ]);
    } catch {
      setMessage(
        "Reading submission could not be saved. Please try again."
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <p className="text-lg font-semibold text-[#3D348B]">
          Loading reading practice...
        </p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="rounded-3xl bg-white p-8 text-red-600 shadow-sm">
        Failed to load reading practice.
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <header className="rounded-[2rem] bg-gradient-to-br from-[#3D348B] via-[#4f46e5] to-[#0f766e] p-8 text-white shadow-lg">
        <div className="flex flex-wrap items-start justify-between gap-6">
          <div className="max-w-3xl space-y-4">
            <div className="inline-flex items-center gap-2 rounded-full bg-white/15 px-4 py-2 text-sm font-semibold">
              <BookOpenText size={16} />
              Reading Practice
            </div>
            <h1 className="text-4xl font-bold tracking-tight">
              Read, choose, and check your comprehension.
            </h1>
            <p className="max-w-2xl text-white/85">
              Work through one passage and 5 multiple-choice questions. Your score, answer key, and feedback will be saved to your practice history.
            </p>
          </div>
          <div className="rounded-3xl bg-white/15 p-5 backdrop-blur">
            <div className="flex items-center gap-2 text-sm font-semibold text-white/80">
              <Clock3 size={16} />
              Estimated time
            </div>
            <div className="mt-2 text-3xl font-bold">
              {data.estimated_minutes} min
            </div>
          </div>
        </div>
      </header>

      {message && (
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-amber-800">
          {message}
        </div>
      )}

      <section className="rounded-3xl bg-white p-8 shadow-sm">
        <h2 className="text-2xl font-bold text-[#3D348B]">
          Passage
        </h2>
        <div className="mt-5 whitespace-pre-line rounded-3xl bg-[#F5F6FC] p-6 leading-8 text-slate-700">
          {data.passage.text}
        </div>
      </section>

      <section className="space-y-5">
        {data.questions.map((question, index) => {
          const selected = answers[question.id] ?? "";

          return (
            <article
              className="rounded-3xl bg-white p-8 shadow-sm"
              key={question.id}
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-sm font-semibold uppercase tracking-[0.2em] text-[#4f46e5]">
                    Question {index + 1}
                  </p>
                  <h3 className="mt-2 text-xl font-bold text-[#3D348B]">
                    {question.question}
                  </h3>
                </div>
                {result?.correct_answers[question.id] && (
                  <div className="flex items-center gap-2 rounded-full bg-emerald-50 px-4 py-2 text-sm font-semibold text-emerald-700">
                    <CheckCircle2 size={16} />
                    Correct answer available
                  </div>
                )}
              </div>

              <div className="mt-6 grid gap-3 md:grid-cols-2">
                {question.options.map((option) => {
                  const isSelected = selected === option;
                  const isCorrect =
                    result?.correct_answers[question.id] === option;
                  const showFeedback = Boolean(result);

                  return (
                    <button
                      key={option}
                      type="button"
                      onClick={() =>
                        handleSelect(question.id, option)
                      }
                      className={[
                        "rounded-2xl border px-4 py-4 text-left transition",
                        isSelected
                          ? "border-[#3D348B] bg-[#EEF2FF] shadow-sm"
                          : "border-slate-200 bg-white hover:border-[#9ca3af] hover:bg-slate-50",
                        showFeedback && isCorrect
                          ? "border-emerald-500 bg-emerald-50"
                          : "",
                      ].join(" ")}
                    >
                      <div className="flex items-start gap-3">
                        <span className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[#3D348B] text-sm font-bold text-white">
                          {String.fromCharCode(65 + question.options.indexOf(option))}
                        </span>
                        <span className="leading-7 text-slate-700">
                          {option}
                        </span>
                      </div>
                    </button>
                  );
                })}
              </div>

              {result && (
                <div className="mt-6 grid gap-4 rounded-2xl bg-[#F5F6FC] p-5 md:grid-cols-3">
                  <InfoBox
                    label="Your answer"
                    value={result.user_answers[question.id] ?? "No answer"}
                  />
                  <InfoBox
                    label="Correct answer"
                    value={result.correct_answers[question.id]}
                  />
                  <InfoBox
                    label="Result"
                    value={
                      result.user_answers[question.id] ===
                      result.correct_answers[question.id]
                        ? "Correct"
                        : "Review"
                    }
                  />
                </div>
              )}

              {result && (
                <p className="mt-4 leading-7 text-slate-600">
                  {result.explanations[question.id]}
                </p>
              )}
            </article>
          );
        })}
      </section>

      <section className="rounded-3xl bg-white p-8 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold text-[#3D348B]">
              Submit your answers
            </h2>
            <p className="mt-2 text-gray-500">
              Your response will be scored and stored in your practice history.
            </p>
          </div>
          <button
            type="button"
            disabled={isSubmitting}
            onClick={handleSubmit}
            className="rounded-xl bg-[#3D348B] px-6 py-3 font-semibold text-white transition hover:bg-[#2d2770] disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isSubmitting ? "Submitting..." : "Submit answers"}
          </button>
        </div>

        {result && (
          <div className="mt-6 grid gap-4 lg:grid-cols-3">
            <InfoBox label="Score" value={`${result.score}/5`} />
            <InfoBox
              label="Feedback"
              value={result.feedback}
            />
            <InfoBox
              label="Passage"
              value={data.passage.title}
            />
          </div>
        )}
      </section>
    </div>
  );
}

function InfoBox({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-2xl bg-white p-4 shadow-sm">
      <p className="text-sm text-gray-500">{label}</p>
      <p className="mt-2 font-semibold text-[#3D348B]">
        {value}
      </p>
    </div>
  );
}
