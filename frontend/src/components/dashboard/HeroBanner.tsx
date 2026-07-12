import { Sparkles } from "lucide-react";

export default function HeroBanner() {
  return (
    <div className="rounded-3xl bg-gradient-to-r from-[#3D348B] to-[#4CB1FF] p-8 text-white shadow-lg">
      <div className="flex items-center gap-3">
        <Sparkles size={32} />
        <div>
          <h1 className="text-3xl font-bold">
            Good Evening, Adeesha 👋
          </h1>

          <p className="mt-2 text-white/90">
            You're on a <strong>12-day learning streak</strong>.
            Keep practicing to reach your weekly goal.
          </p>
        </div>
      </div>
    </div>
  );
}