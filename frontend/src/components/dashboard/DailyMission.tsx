import { CheckCircle2 } from "lucide-react";

export default function DailyMission() {
  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-xl font-bold text-[#3D348B]">
        Today's Mission
      </h2>

      <div className="space-y-3">
        <div className="flex items-center gap-3">
          <CheckCircle2 className="text-[#4CB1FF]" />
          <span>Complete 2 Grammar exercises</span>
        </div>

        <div className="flex items-center gap-3">
          <CheckCircle2 className="text-[#4CB1FF]" />
          <span>Practice Speaking for 10 minutes</span>
        </div>

        <div className="flex items-center gap-3">
          <CheckCircle2 className="text-[#4CB1FF]" />
          <span>Learn 5 new vocabulary words</span>
        </div>
      </div>
    </div>
  );
}