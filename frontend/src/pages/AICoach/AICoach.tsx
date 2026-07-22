import { useEffect, useMemo, useRef, useState } from "react";
import { Bot, Lightbulb, Send, Sparkles, User } from "lucide-react";
import { useAICoach, useSendAICoachMessage } from "../../hooks/useAICoach";

export default function AICoach() {
  const { data, isLoading, error } = useAICoach();
  const sendMessage = useSendAICoachMessage();
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement | null>(null);

  const history = useMemo(
    () => data?.conversation_history ?? [],
    [data?.conversation_history]
  );

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [history, data?.reply, sendMessage.isPending]);

  const submitMessage = async (message: string) => {
    const text = message.trim();
    if (!text) return;
    setInput("");
    await sendMessage.mutateAsync({ message: text });
  };

  const latestSummary = data?.current_learner_summary;

  if (isLoading) {
    return (
      <div className="flex min-h-[70vh] items-center justify-center">
        <h1 className="text-xl font-semibold text-[#3D348B]">
          Loading AI coach...
        </h1>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex min-h-[70vh] items-center justify-center">
        <h1 className="text-xl font-semibold text-red-500">
          Failed to load AI coach.
        </h1>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <header className="rounded-[2rem] bg-gradient-to-br from-[#3D348B] via-[#4f46e5] to-[#0f766e] p-8 text-white shadow-lg">
        <div className="flex flex-wrap items-start justify-between gap-6">
          <div className="max-w-3xl space-y-4">
            <div className="inline-flex items-center gap-2 rounded-full bg-white/15 px-4 py-2 text-sm font-semibold">
              <Sparkles size={16} />
              AI Coach
            </div>
            <h1 className="text-4xl font-bold tracking-tight">
              Your personal study mentor
            </h1>
            <p className="max-w-2xl text-white/85">
              Personalized coaching based on your learning path, analytics,
              practice history, and recent mistakes.
            </p>
          </div>
          <div className="rounded-3xl bg-white/15 p-5 backdrop-blur">
            <div className="text-sm font-semibold text-white/80">
              Current Level
            </div>
            <div className="mt-2 text-3xl font-bold">
              {latestSummary?.current_level ?? "B1"}
            </div>
          </div>
        </div>
      </header>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <SummaryCard title="Current Focus" value={latestSummary?.current_focus ?? "Reading"} />
        <SummaryCard title="Recommended Practice" value={latestSummary?.recommended_practice ?? "Vocabulary"} />
        <SummaryCard title="Average Score" value={`${latestSummary?.average_score ?? 0}%`} />
        <SummaryCard title="Overall Progress" value={`${latestSummary?.overall_progress ?? 0}%`} />
      </section>

      <section className="grid gap-8 xl:grid-cols-[1.6fr_1fr]">
        <div className="rounded-3xl bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <Bot className="text-[#3D348B]" size={24} />
            <h2 className="text-xl font-bold text-[#3D348B]">
              Conversation
            </h2>
          </div>

          <div className="mt-6 max-h-[560px] space-y-4 overflow-y-auto pr-2">
            {history.map((item) => (
              <ChatBubble
                key={`${item.role}-${item.created_at}-${item.message.slice(0, 20)}`}
                role={item.role}
                message={item.message}
              />
            ))}

            {sendMessage.isPending && (
              <ChatBubble role="assistant" message="Thinking through your data..." />
            )}

            {data.reply && (!history.length || history[history.length - 1]?.message !== data.reply) && (
              <ChatBubble role="assistant" message={data.reply} />
            )}

            <div ref={bottomRef} />
          </div>

          <form
            className="mt-6 flex gap-3"
            onSubmit={(event) => {
              event.preventDefault();
              void submitMessage(input);
            }}
          >
            <input
              value={input}
              onChange={(event) => setInput(event.target.value)}
              placeholder="Ask for guidance about your learning..."
              className="min-h-12 flex-1 rounded-2xl border border-slate-200 px-4 outline-none focus:border-[#3D348B]"
            />
            <button
              type="submit"
              disabled={sendMessage.isPending}
              className="inline-flex items-center gap-2 rounded-2xl bg-[#3D348B] px-5 py-3 font-semibold text-white transition hover:bg-[#2d2770] disabled:cursor-not-allowed disabled:opacity-60"
            >
              <Send size={18} />
              {sendMessage.isPending ? "Sending..." : "Send"}
            </button>
          </form>

          {sendMessage.isError && (
            <p className="mt-4 text-sm text-red-600">
              The coach could not respond. Please try again.
            </p>
          )}
        </div>

        <div className="space-y-6">
          <div className="rounded-3xl bg-white p-6 shadow-sm">
            <div className="flex items-center gap-3">
              <Lightbulb className="text-[#3D348B]" size={22} />
              <h2 className="text-lg font-bold text-[#3D348B]">
                Suggested Questions
              </h2>
            </div>
            <div className="mt-4 space-y-3">
              {data.suggested_questions.map((question) => (
                <button
                  key={question}
                  type="button"
                  onClick={() => void submitMessage(question)}
                  className="w-full rounded-2xl bg-[#F5F6FC] px-4 py-3 text-left text-sm font-medium text-[#4A4B4B] transition hover:bg-[#D0E6FF]"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>

          <div className="rounded-3xl bg-white p-6 shadow-sm">
            <h2 className="text-lg font-bold text-[#3D348B]">
              Current Learner Summary
            </h2>
            <div className="mt-4 space-y-3 text-sm text-slate-600">
              <SummaryLine label="Focus" value={latestSummary?.current_focus ?? "No data"} />
              <SummaryLine label="Weak Skills" value={(latestSummary?.weak_skills ?? []).join(", ") || "No data"} />
              <SummaryLine label="Strong Skills" value={(latestSummary?.strong_skills ?? []).join(", ") || "No data"} />
              <SummaryLine label="Next Action" value={data.recommended_next_action.description} />
            </div>
          </div>

          <div className="rounded-3xl bg-white p-6 shadow-sm">
            <div className="flex items-center gap-3">
              <User className="text-[#3D348B]" size={22} />
              <h2 className="text-lg font-bold text-[#3D348B]">
                Recommended Next Action
              </h2>
            </div>
            <p className="mt-4 font-semibold text-[#3D348B]">
              {data.recommended_next_action.title}
            </p>
            <p className="mt-2 text-sm leading-7 text-slate-600">
              {data.recommended_next_action.description}
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}

function ChatBubble({
  role,
  message,
}: {
  role: "user" | "assistant";
  message: string;
}) {
  const isUser = role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={[
          "max-w-[80%] rounded-3xl px-5 py-4 shadow-sm",
          isUser
            ? "bg-[#3D348B] text-white"
            : "bg-[#F5F6FC] text-slate-700",
        ].join(" ")}
      >
        <div className="mb-2 flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.2em] opacity-70">
          {isUser ? <User size={14} /> : <Bot size={14} />}
          {isUser ? "You" : "Coach"}
        </div>
        <p className="whitespace-pre-line leading-7">{message}</p>
      </div>
    </div>
  );
}

function SummaryCard({
  title,
  value,
}: {
  title: string;
  value: string;
}) {
  return (
    <div className="rounded-2xl bg-white p-6 shadow-sm">
      <p className="text-sm text-gray-500">{title}</p>
      <h3 className="mt-2 text-2xl font-bold text-[#3D348B]">{value}</h3>
    </div>
  );
}

function SummaryLine({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-2xl bg-[#F5F6FC] px-4 py-3">
      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[#4f46e5]">
        {label}
      </p>
      <p className="mt-1">{value}</p>
    </div>
  );
}
