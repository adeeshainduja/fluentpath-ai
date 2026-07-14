interface OverallScoreCardProps {
  score: number;
}

export default function OverallScoreCard({
  score,
}: OverallScoreCardProps) {
  return (
    <div className="rounded-3xl bg-white p-8 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-500">
            Overall English Score
          </p>

          <h2 className="mt-2 text-6xl font-bold text-[#3D348B]">
            {score}%
          </h2>
        </div>

        <div className="flex h-20 w-20 items-center justify-center rounded-full bg-blue-50">
          <span className="text-2xl font-bold text-[#3D348B]">
            {score}
          </span>
        </div>
      </div>

      <div className="mt-8 h-3 w-full rounded-full bg-gray-200">
        <div
          className="h-3 rounded-full bg-gradient-to-r from-[#3D348B] to-[#4CB1FF] transition-all duration-700"
          style={{
            width: `${score}%`,
          }}
        />
      </div>

      <p className="mt-4 text-sm text-gray-500">
        Your overall performance across all completed practice sessions.
      </p>
    </div>
  );
}