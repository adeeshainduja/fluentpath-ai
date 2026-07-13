import { CheckCircle2 } from "lucide-react";

export default function DailyMission() {
  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">
      <h2 className="text-xl font-bold text-[#3D348B]">
        Today's Mission
      </h2>

      <div className="mt-6 space-y-4">

        <div className="flex items-center justify-between">
          <span>Complete 2 Writing Tasks</span>
          <CheckCircle2 className="text-green-500" />
        </div>

        <div className="flex items-center justify-between">
          <span>Learn 10 New Words</span>
          <span className="text-gray-400">0/10</span>
        </div>

        <div className="flex items-center justify-between">
          <span>Practice Speaking (5 min)</span>
          <span className="text-gray-400">0/5</span>
        </div>

      </div>

      <button className="mt-6 w-full rounded-xl bg-[#3D348B] py-3 text-white hover:bg-[#2f2773]">
        Continue
      </button>
    </div>
  );
}