interface WeeklyActivityProps {
  days: {
    day: string;
    score: number;
  }[];
}

export default function WeeklyActivityChart({
  days,
}: WeeklyActivityProps) {
  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">

      <h2 className="mb-6 text-2xl font-bold text-[#3D348B]">
        Weekly Activity
      </h2>

      <div className="grid grid-cols-7 gap-4">

        {days.map((day) => (
          <div
            key={day.day}
            className="text-center"
          >
            <div
              className="mx-auto mb-3 flex h-20 w-12 items-end rounded-lg bg-gray-200"
            >
              <div
                className="w-full rounded-lg bg-[#4CB1FF]"
                style={{
                  height: `${day.score}%`,
                }}
              />
            </div>

            <p className="text-sm text-gray-500">
              {day.day}
            </p>
          </div>
        ))}

      </div>

    </div>
  );
}