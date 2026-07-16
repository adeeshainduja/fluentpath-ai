import {
  Mic,
  Square,
  RotateCcw,
  Send,
  Volume2,
} from "lucide-react";
import { useRef, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";

import { useAuth } from "../../hooks/useAuth";
import { evaluateSpeaking } from "../../services/speakingApi";
import type { SpeakingResponse } from "../../types/speaking";

type SpeechRecognitionEventLike = Event & {
  results: {
    length: number;
    [index: number]: {
      isFinal: boolean;
      [index: number]: {
        transcript: string;
      };
    };
  };
};

type BrowserSpeechRecognition = {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  start: () => void;
  stop: () => void;
  onresult:
    | ((event: SpeechRecognitionEventLike) => void)
    | null;
  onerror: (() => void) | null;
  onend: (() => void) | null;
};

type SpeechRecognitionConstructor = new () => BrowserSpeechRecognition;

declare global {
  interface Window {
    SpeechRecognition?: SpeechRecognitionConstructor;
    webkitSpeechRecognition?: SpeechRecognitionConstructor;
  }
}

const getSpeechRecognition = () =>
  window.SpeechRecognition ?? window.webkitSpeechRecognition;

export default function SpeakingPractice() {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const recognitionRef =
    useRef<BrowserSpeechRecognition | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [interimTranscript, setInterimTranscript] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [feedback, setFeedback] =
    useState<SpeakingResponse | null>(null);
  const [message, setMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const startRecording = async () => {
    setMessage("");
    setFeedback(null);
    setInterimTranscript("");
    audioChunksRef.current = [];

    const Recognition = getSpeechRecognition();

    if (!Recognition) {
      setMessage(
        "Speech recognition is not available in this browser. Try Chrome or Edge."
      );
      return;
    }

    try {
      const stream =
        await navigator.mediaDevices.getUserMedia({
          audio: true,
        });

      const recorder = new MediaRecorder(stream);

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      recorder.onstop = () => {
        const audioBlob = new Blob(
          audioChunksRef.current,
          {
            type: "audio/webm",
          }
        );

        if (audioUrl) {
          URL.revokeObjectURL(audioUrl);
        }

        setAudioUrl(URL.createObjectURL(audioBlob));
        stream
          .getTracks()
          .forEach((track) => track.stop());
      };

      const recognition = new Recognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = "en-US";

      recognition.onresult = (event) => {
        let finalText = "";
        let interimText = "";

        for (
          let index = 0;
          index < event.results.length;
          index += 1
        ) {
          const result = event.results[index];
          const text = result[0].transcript;

          if (result.isFinal) {
            finalText += `${text} `;
          } else {
            interimText += text;
          }
        }

        if (finalText.trim()) {
          setTranscript((current) =>
            `${current} ${finalText}`.trim()
          );
        }

        setInterimTranscript(interimText);
      };

      recognition.onerror = () => {
        setMessage(
          "Speech recognition stopped unexpectedly. You can start again or edit the transcript manually."
        );
      };

      recognition.onend = () => {
        setInterimTranscript("");
      };

      mediaRecorderRef.current = recorder;
      recognitionRef.current = recognition;

      recorder.start();
      recognition.start();
      setIsRecording(true);
    } catch {
      setMessage(
        "Microphone access was denied or unavailable."
      );
    }
  };

  const stopRecording = () => {
    recognitionRef.current?.stop();
    mediaRecorderRef.current?.stop();
    setIsRecording(false);
  };

  const resetSession = () => {
    if (isRecording) {
      stopRecording();
    }

    if (audioUrl) {
      URL.revokeObjectURL(audioUrl);
    }

    setTranscript("");
    setInterimTranscript("");
    setAudioUrl("");
    setFeedback(null);
    setMessage("");
  };

  const submitTranscript = async () => {
    if (!transcript.trim()) {
      setMessage(
        "Record or enter a transcript before requesting feedback."
      );
      return;
    }

    setIsSubmitting(true);
    setMessage("");

    try {
      const result = await evaluateSpeaking(
        transcript.trim(),
        user?.id
      );

      setFeedback(result);
      setTranscript(result.transcript);

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
      ]);
    } catch {
      setMessage(
        "Speaking feedback could not be generated. Check your AI service configuration and try again."
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-[#3D348B]">
          Speaking Practice
        </h1>
        <p className="mt-2 text-gray-500">
          Record your answer, review the transcript, and get AI feedback on pronunciation, fluency, grammar, and vocabulary.
        </p>
      </div>

      {message && (
        <div className="rounded-xl border border-amber-200 bg-amber-50 p-4 text-amber-700">
          {message}
        </div>
      )}

      <section className="rounded-3xl bg-white p-8 shadow-sm">
        <div className="flex flex-wrap items-center gap-3">
          {!isRecording ? (
            <button
              className="flex items-center gap-2 rounded-xl bg-[#3D348B] px-5 py-3 font-semibold text-white transition hover:bg-[#2d2770]"
              type="button"
              onClick={startRecording}
            >
              <Mic size={18} />
              Start recording
            </button>
          ) : (
            <button
              className="flex items-center gap-2 rounded-xl bg-red-600 px-5 py-3 font-semibold text-white transition hover:bg-red-700"
              type="button"
              onClick={stopRecording}
            >
              <Square size={18} />
              Stop recording
            </button>
          )}

          <button
            className="flex items-center gap-2 rounded-xl bg-[#F5F6FC] px-5 py-3 font-semibold text-[#3D348B] transition hover:bg-[#D0E6FF]"
            type="button"
            onClick={resetSession}
          >
            <RotateCcw size={18} />
            Reset
          </button>

          <button
            className="flex items-center gap-2 rounded-xl bg-[#FFD166] px-5 py-3 font-semibold text-[#3D348B] transition hover:bg-[#f4bf3e] disabled:opacity-60"
            disabled={isSubmitting || isRecording}
            type="button"
            onClick={submitTranscript}
          >
            <Send size={18} />
            {isSubmitting ? "Evaluating..." : "Get feedback"}
          </button>
        </div>

        {audioUrl && (
          <div className="mt-6 rounded-2xl bg-[#F5F6FC] p-4">
            <div className="mb-3 flex items-center gap-2 font-semibold text-[#3D348B]">
              <Volume2 size={18} />
              Recording playback
            </div>
            <audio
              className="w-full"
              controls
              src={audioUrl}
            />
          </div>
        )}

        <label className="mt-6 block space-y-3">
          <span className="text-lg font-bold text-[#3D348B]">
            Transcript
          </span>
          <textarea
            className="h-64 w-full resize-none rounded-2xl border border-gray-200 bg-[#F5F6FC] p-4 leading-8 outline-none transition focus:border-[#3D348B] focus:bg-white"
            placeholder="Your speech transcript will appear here. You can edit it before evaluation."
            value={
              interimTranscript
                ? `${transcript} ${interimTranscript}`.trim()
                : transcript
            }
            onChange={(event) =>
              setTranscript(event.target.value)
            }
          />
        </label>
      </section>

      {feedback && (
        <section className="rounded-3xl bg-white p-8 shadow-sm">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <h2 className="text-2xl font-bold text-[#3D348B]">
                AI Speaking Feedback
              </h2>
              <p className="mt-2 text-gray-500">
                {feedback.coach_message}
              </p>
            </div>
            <div className="rounded-2xl bg-[#D0E6FF] px-6 py-4 text-center">
              <p className="text-sm font-semibold text-[#3D348B]">
                Overall
              </p>
              <p className="text-3xl font-bold text-[#3D348B]">
                {feedback.score}
              </p>
            </div>
          </div>

          <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-5">
            {[
              [
                "Pronunciation",
                feedback.evaluation.pronunciation_score,
              ],
              [
                "Fluency",
                feedback.evaluation.fluency_score,
              ],
              [
                "Grammar",
                feedback.evaluation.grammar_score,
              ],
              [
                "Vocabulary",
                feedback.evaluation.vocabulary_score,
              ],
              [
                "Confidence",
                feedback.evaluation.confidence_score,
              ],
            ].map(([label, score]) => (
              <div
                className="rounded-2xl bg-[#F5F6FC] p-4"
                key={label}
              >
                <p className="text-sm text-gray-500">
                  {label}
                </p>
                <p className="mt-2 text-2xl font-bold text-[#3D348B]">
                  {score}
                </p>
              </div>
            ))}
          </div>

          <div className="mt-8 grid gap-5 lg:grid-cols-2">
            <FeedbackBlock
              title="Pronunciation"
              value={
                feedback.evaluation.pronunciation_feedback
              }
            />
            <FeedbackBlock
              title="Fluency"
              value={feedback.evaluation.fluency_feedback}
            />
            <FeedbackBlock
              title="Grammar"
              value={feedback.evaluation.grammar_feedback}
            />
            <FeedbackBlock
              title="Vocabulary"
              value={
                feedback.evaluation.vocabulary_feedback
              }
            />
          </div>

          <div className="mt-8 rounded-2xl bg-[#F5F6FC] p-5">
            <h3 className="font-bold text-[#3D348B]">
              Next steps
            </h3>
            <ul className="mt-3 list-disc space-y-2 pl-5">
              {feedback.evaluation.suggestions.map(
                (suggestion) => (
                  <li key={suggestion}>{suggestion}</li>
                )
              )}
            </ul>
          </div>
        </section>
      )}
    </div>
  );
}

function FeedbackBlock({
  title,
  value,
}: {
  title: string;
  value: string;
}) {
  return (
    <div className="rounded-2xl border border-gray-100 p-5">
      <h3 className="font-bold text-[#3D348B]">
        {title}
      </h3>
      <p className="mt-3 leading-7 text-gray-600">
        {value}
      </p>
    </div>
  );
}
