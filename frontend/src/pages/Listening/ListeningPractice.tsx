import { useEffect, useMemo, useRef, useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import {
  PauseCircle,
  PlayCircle,
  Headphones,
  Volume2,
  CheckCircle2,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../../hooks/useAuth";
import {
  generateListeningPractice,
  submitListeningPractice,
} from "../../services/listeningApi";
import type {
  ListeningPractice,
  ListeningSubmissionResponse,
} from "../../types/listening";

type AnswerMap = Record<number, string>;

export default function ListeningPractice() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [answers, setAnswers] = useState<AnswerMap>({});
  const [result, setResult] =
    useState<ListeningSubmissionResponse | null>(null);
  const [message, setMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);

  const { data, isLoading, error } = useQuery<ListeningPractice>({
    queryKey: ["listening-practice", user?.id ?? "me"],
    queryFn: generateListeningPractice,
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
      setIsPlaying(false);
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.currentTime = 0;
      }
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

  const togglePlayback = async () => {
    if (!audioRef.current) return;
    if (audioRef.current.paused) {
      await audioRef.current.play();
      setIsPlaying(true);
    } else {
      audioRef.current.pause();
      setIsPlaying(false);
    }
  };

  const handleSubmit = async () => {
    if (!data) return;

    if (!allAnswered) {
      setMessage("Please answer all 5 questions before submitting.");
      return;
    }

    setIsSubmitting(true);
    setMessage("");

    try {
      const submission = await submitListeningPractice({
        learner_id: user?.id,
        practice_id: data.practice_id,
        answers,
      });

      setResult(submission);
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ["dashboard"] }),
        queryClient.invalidateQueries({ queryKey: ["history"] }),
        queryClient.invalidateQueries({ queryKey: ["analytics"] }),
      ]);
    } catch {
      setMessage(
        "Listening submission could not be saved. Please try again."
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <p className="text-lg font-semibold text-[#3D348B]">
          Loading listening practice...
        </p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="rounded-3xl bg-white p-8 text-red-600 shadow-sm">
        Failed to load listening practice.
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <header className="rounded-[2rem] bg-gradient-to-br from-[#111827] via-[#312e81] to-[#3b82f6] p-8 text-white shadow-lg">
        <div className="flex flex-wrap items-start justify-between gap-6">
          <div className="max-w-3xl space-y-4">
            <div className="inline-flex items-center gap-2 rounded-full bg-white/15 px-4 py-2 text-sm font-semibold">
              <Headphones size={16} />
              Listening Practice
            </div>
            <h1 className="text-4xl font-bold tracking-tight">
              Listen carefully, then answer the questions.
            </h1>
            <p className="max-w-2xl text-white/85">
              Use the audio player or the play and pause controls, then answer 5 multiple-choice questions based on the transcript.
            </p>
          </div>
          <div className="rounded-3xl bg-white/15 p-5 backdrop-blur">
            <div className="flex items-center gap-2 text-sm font-semibold text-white/80">
              <Volume2 size={16} />
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
          Audio
        </h2>
        <p className="mt-2 text-gray-500">
          Transcript for internal scoring is hidden here as a practice aid after submission.
        </p>

        <div className="mt-6 rounded-3xl bg-[#F5F6FC] p-6">
          <audio
            ref={audioRef}
            className="hidden"
            controls
            src={data.audio_url}
            onPlay={() => setIsPlaying(true)}
            onPause={() => setIsPlaying(false)}
            onEnded={() => setIsPlaying(false)}
          />
          <div className="flex flex-wrap items-center gap-4">
            <button
              type="button"
              onClick={togglePlayback}
              className="inline-flex items-center gap-2 rounded-xl bg-[#3D348B] px-5 py-3 font-semibold text-white transition hover:bg-[#2d2770]"
            >
              {isPlaying ? <PauseCircle size={20} /> : <PlayCircle size={20} />}
              {isPlaying ? "Pause" : "Play"}
            </button>
            <div className="text-sm text-slate-600">
              Audio player is available below and uses the bundled sample mp3.
            </div>
          </div>
          <audio
            className="mt-5 w-full"
            controls
            src={data.audio_url}
            onPlay={() => setIsPlaying(true)}
            onPause={() => setIsPlaying(false)}
            onEnded={() => setIsPlaying(false)}
          />
          <p className="mt-5 whitespace-pre-line rounded-2xl bg-white p-4 leading-7 text-slate-700">
            {data.transcript}
          </p>
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
                  <p className="text-sm font-semibold uppercase tracking-[0.2em] text-[#2563eb]">
                    Question {index + 1}
                  </p>
                  <h3 className="mt-2 text-xl font-bold text-[#3D348B]">
                    {question.question}
                  </h3>
                </div>
                {result?.correct_answers[question.id] && (
                  <div className="flex items-center gap-2 rounded-full bg-emerald-50 px-4 py-2 text-sm font-semibold text-emerald-700">
                    <CheckCircle2 size={16} />
                    Answer key ready
                  </div>
                )}
              </div>

              <div className="mt-6 grid gap-3 md:grid-cols-2">
                {question.options.map((option, optionIndex) => {
                  const isSelected = selected === option;
                  const isCorrect =
                    result?.correct_answers[question.id] === option;
                  const showFeedback = Boolean(result);

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
                        showFeedback && isCorrect
                          ? "border-emerald-500 bg-emerald-50"
                          : "",
                      ].join(" ")}
                    >
                      <div className="flex items-start gap-3">
                        <span className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[#3D348B] text-sm font-bold text-white">
                          {String.fromCharCode(65 + optionIndex)}
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
              Your response will be scored and saved to history, dashboard, and analytics.
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
          <div className="mt-6 grid gap-4 lg:grid-cols-4">
            <InfoBox label="Score" value={`${result.score}/100`} />
            <InfoBox label="AI feedback" value={result.ai_feedback} />
            <InfoBox label="Transcript" value={result.transcript} />
            <InfoBox label="Audio" value={result.audio_url} />
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
      <p className="mt-2 break-words font-semibold text-[#3D348B]">
        {value}
      </p>
    </div>
  );
}
