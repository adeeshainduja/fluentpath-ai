import { Target } from "lucide-react";

export default function GoalCard() {
  return (
    <div className="rounded-3xl bg-white p-8 shadow-sm">

      <div className="flex items-center gap-3">

        <Target
          size={24}
          className="text-[#3D348B]"
        />

        <h2 className="text-xl font-bold">
          Weekly Goal
        </h2>

      </div>

      <div className="mt-8">

        <div className="mb-2 flex justify-between">

          <span>7 / 10 Sessions</span>

          <span>70%</span>

        </div>

        <div className="h-3 rounded-full bg-[#D0E6FF]">

          <div
            className="h-3 rounded-full bg-[#4CB1FF]"
            style={{
              width: "70%",
            }}
          />

        </div>

      </div>

    </div>
  );
}