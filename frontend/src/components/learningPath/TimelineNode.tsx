import {
  CheckCircle2,
  Lock,
  PlayCircle,
  Clock,
  ArrowRight,
} from "lucide-react";

interface TimelineNodeProps {
  title: string;
  skill: string;
  difficulty: string;
  estimatedMinutes?: number;
  status: "completed" | "current" | "locked";
  isLast?: boolean;
}

export default function TimelineNode({
  title,
  skill,
  difficulty,
  estimatedMinutes = 20,
  status,
  isLast = false,
}: TimelineNodeProps) {
  return (
    <div className="relative flex items-start gap-6">

      {/* Timeline Line */}
      {!isLast && (
        <div className="absolute left-6 top-16 h-20 w-1 rounded-full bg-slate-200"></div>
      )}

      {/* Status Icon */}
      <div
        className={`relative z-10 flex h-12 w-12 items-center justify-center rounded-full shadow-md ${
          status === "completed"
            ? "bg-green-500 text-white"
            : status === "current"
            ? "bg-gradient-to-br from-[#4CB1FF] to-[#3D348B] text-white"
            : "bg-gray-300 text-white"
        }`}
      >
        {status === "completed" && <CheckCircle2 size={24} />}

        {status === "current" && <PlayCircle size={24} />}

        {status === "locked" && <Lock size={22} />}
      </div>

      {/* Card */}
      <div
        className={`flex-1 rounded-2xl border p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg ${
          status === "completed"
            ? "border-green-200 bg-green-50"
            : status === "current"
            ? "border-[#4CB1FF] bg-gradient-to-r from-blue-50 to-indigo-50"
            : "border-slate-200 bg-slate-50"
        }`}
      >
        <div className="flex items-center justify-between">

          <div>
            <h3 className="text-xl font-bold text-[#3D348B]">
              {title}
            </h3>

            <p className="mt-1 text-gray-500">
              {skill} • {difficulty}
            </p>
          </div>

          <span
            className={`rounded-full px-4 py-2 text-sm font-semibold ${
              status === "completed"
                ? "bg-green-100 text-green-700"
                : status === "current"
                ? "bg-blue-100 text-blue-700"
                : "bg-gray-200 text-gray-600"
            }`}
          >
            {status === "completed"
              ? "Completed"
              : status === "current"
              ? "Current"
              : "Locked"}
          </span>
        </div>

        {/* Footer */}
        <div className="mt-6 flex items-center justify-between">

          <div className="flex items-center gap-2 text-sm text-gray-500">
            <Clock size={16} />
            {estimatedMinutes} min
          </div>

          {status === "current" && (
            <button className="flex items-center gap-2 rounded-xl bg-[#3D348B] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[#2d2668]">
              Continue
              <ArrowRight size={16} />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}