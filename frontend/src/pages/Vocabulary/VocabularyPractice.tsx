import { useEffect, useMemo, useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Languages, CheckCircle2, ArrowRight } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../../hooks/useAuth";
import {
  generateVocabularyPractice,
  submitVocabularyPractice,
} from "../../services/vocabularyApi";
import type {
  VocabularyPractice,
  VocabularySubmissionResponse,
} from "../../types/vocabulary";

type AnswerMap = Record<number, string>;

export default function VocabularyPractice() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [answers, setAnswers] = useState<AnswerMap>({});
  const [result, setResult] =
    useState<VocabularySubmissionResponse | null>(null);
  const [message, setMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { data, isLoading, error } = useQuery<VocabularyPractice>({
    queryKey: ["vocabulary-practice", user?.id ?? "me"],
    queryFn: generateVocabularyPractice,
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
        Object.fromEntries(data.questions.map((question) => [question.id, ""]))
      );
      setResult(null);
      setMessage("");
    }
  }, [data]);

  const allAnswered = useMemo(
    () => data?.questions.every((question) => Boolean(answers[question.id])) ?? false,
    [answers, data]
  );

  const handleSelect = (questionId: number, value: string) => {
    setAnswers((current) => ({
      ...current,
      [questionId]: value,
    }));
  };

  const handleSubmit = async () => {
    if (!data) return;

    if (!allAnswered) {
      setMessage("Please answer all questions before submitting.");
      return;
    }

    setIsSubmitting(true);
    setMessage("");

    try {
      const submission = await submitVocabularyPractice({
        sessionId: data.sessionId,
        answers: data.questions.map((question) => ({
          questionId: question.id,
          selectedOption: answers[question.id] ?? "",
        })),
      });

      setResult(submission);
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ["dashboard"] }),
        queryClient.invalidateQueries({ queryKey: ["history"] }),
        queryClient.invalidateQueries({ queryKey: ["analytics"] }),
      ]);
    } catch {
      setMessage("Vocabulary submission could not be saved. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <p className="text-lg font-semibold text-[#3D348B]">
          Loading vocabulary practice...
        </p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="rounded-3xl bg-white p-8 text-red-600 shadow-sm">
        Failed to load vocabulary practice.
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <header className="rounded-[2rem] bg-gradient-to-br from-[#7c3aed] via-[#4f46e5] to-[#0f766e] p-8 text-white shadow-lg">
        <div className="flex flex-wrap items-start justify-between gap-6">
          <div className="max-w-3xl space-y-4">
            <div className="inline-flex items-center gap-2 rounded-full bg-white/15 px-4 py-2 text-sm font-semibold">
              <Languages size={16} />
              Vocabulary Practice
            </div>
            <h1 className="text-4xl font-bold tracking-tight">
              Build word knowledge with quick multiple-choice practice.
            </h1>
            <p className="max-w-2xl text-white/85">
              Review one word at a time, choose the best meaning, and get instant feedback after submission.
            </p>
          </div>
          <div className="rounded-3xl bg-white/15 p-5 backdrop-blur">
            <div className="text-sm font-semibold text-white/80">
              Difficulty
            </div>
            <div className="mt-2 text-3xl font-bold">{data.difficulty}</div>
          </div>
        </div>
        <div className="mt-6 h-2 overflow-hidden rounded-full bg-white/20">
          <div
            className="h-full rounded-full bg-white transition-all"
            style={{
              width: `${(Object.values(answers).filter(Boolean).length / data.questions.length) * 100}%`,
            }}
          />
        </div>
      </header>

      {message && (
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-amber-800">
          {message}
        </div>
      )}

      {result ? (
        <section className="rounded-3xl bg-white p-8 shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <h2 className="text-2xl font-bold text-[#3D348B]">Result</h2>
              <p className="mt-2 text-gray-500">
                Your vocabulary attempt has been evaluated and saved.
              </p>
            </div>
            <div className="rounded-2xl bg-[#EEF2FF] px-5 py-3 text-[#3D348B]">
              <div className="text-sm font-medium">Score</div>
              <div className="text-3xl font-bold">{result.score}/100</div>
            </div>
          </div>

          <div className="mt-6 grid gap-4 lg:grid-cols-2">
            <InfoBox label="Feedback" value={result.feedback} />
            <InfoBox
              label="Correct answers"
              value={Object.entries(result.correctAnswers)
                .map(([questionId, answer]) => `${questionId}. ${answer}`)
                .join(" | ")}
            />
          </div>

          <div className="mt-6 space-y-4">
            {data.questions.map((question) => (
              <div key={question.id} className="rounded-2xl bg-[#F5F6FC] p-5">
                <div className="flex items-center gap-2 text-sm font-semibold text-[#4f46e5]">
                  <CheckCircle2 size={16} />
                  {question.word}
                </div>
                <p className="mt-2 font-semibold text-[#3D348B]">
                  {result.correctAnswers[question.id]}
                </p>
                <p className="mt-2 leading-7 text-slate-600">
                  {result.explanations[question.id]}
                </p>
              </div>
            ))}
          </div>
        </section>
      ) : (
        <>
          <section className="rounded-3xl bg-white p-8 shadow-sm">
            <div className="flex items-center justify-between gap-4">
              <div>
                <h2 className="text-2xl font-bold text-[#3D348B]">
                  Vocabulary Header
                </h2>
                <p className="mt-2 text-gray-500">
                  Choose the meaning that best matches each word.
                </p>
              </div>
              <div className="rounded-2xl bg-[#EEF2FF] px-4 py-2 text-sm font-semibold text-[#3D348B]">
                {Object.values(answers).filter(Boolean).length}/{data.questions.length} answered
              </div>
            </div>
          </section>

          <section className="space-y-5">
            {data.questions.map((question, index) => {
              const selected = answers[question.id] ?? "";

              return (
                <article key={question.id} className="rounded-3xl bg-white p-8 shadow-sm">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <p className="text-sm font-semibold uppercase tracking-[0.2em] text-[#4f46e5]">
                        Question {index + 1}
                      </p>
                      <h3 className="mt-2 text-2xl font-bold text-[#3D348B]">
                        {question.word}
                      </h3>
                      <p className="mt-2 text-slate-600">{question.question}</p>
                    </div>
                  </div>

                  <div className="mt-6 grid gap-3 md:grid-cols-2">
                    {question.options.map((option, optionIndex) => {
                      const isSelected = selected === option;

                      return (
                        <button
                          key={option}
                          type="button"
                          onClick={() => handleSelect(question.id, option)}
                          className={[
                            "rounded-2xl border px-4 py-4 text-left transition",
                            isSelected
                              ? "border-[#3D348B] bg-[#EEF2FF] shadow-sm"
                              : "border-slate-200 bg-white hover:border-[#9ca3af] hover:bg-slate-50",
                          ].join(" ")}
                        >
                          <div className="flex items-start gap-3">
                            <span className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[#3D348B] text-sm font-bold text-white">
                              {String.fromCharCode(65 + optionIndex)}
                            </span>
                            <span className="leading-7 text-slate-700">{option}</span>
                          </div>
                        </button>
                      );
                    })}
                  </div>
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
                  Your response will be scored and stored in your history, dashboard, and analytics.
                </p>
              </div>
              <button
                type="button"
                disabled={isSubmitting}
                onClick={handleSubmit}
                className="inline-flex items-center gap-2 rounded-xl bg-[#3D348B] px-6 py-3 font-semibold text-white transition hover:bg-[#2d2770] disabled:cursor-not-allowed disabled:opacity-60"
              >
                {isSubmitting ? "Submitting..." : "Submit"}
                <ArrowRight size={18} />
              </button>
            </div>
          </section>
        </>
      )}
    </div>
  );
}

function InfoBox({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl bg-white p-4 shadow-sm">
      <p className="text-sm text-gray-500">{label}</p>
      <p className="mt-2 break-words font-semibold text-[#3D348B]">{value}</p>
    </div>
  );
}
