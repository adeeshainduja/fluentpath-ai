import { Sparkles } from "lucide-react";

export default function RecommendationCard() {
  return (
    <div className="rounded-3xl bg-gradient-to-br from-[#3D348B] to-[#4CB1FF] p-8 text-white shadow-lg">

      <div className="flex items-center gap-3">

        <Sparkles size={28} />

        <h2 className="text-xl font-bold">
          AI Recommendation
        </h2>

      </div>

      <p className="mt-6 text-white/90 leading-7">

        Focus on <strong>Grammar</strong> today.

        Your recent performance shows improvement in
        vocabulary, but grammar accuracy has declined.

      </p>

      <button
        className="mt-8 rounded-xl bg-white px-6 py-3 font-semibold text-[#3D348B] transition hover:scale-105"
      >
        Start Practice
      </button>

    </div>
  );
}