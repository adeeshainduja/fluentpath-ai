interface ErrorStatisticsProps {
  totalErrors: number;
  resolvedErrors: number;
  activeErrors: number;
}

export default function ErrorStatisticsCard({
  totalErrors,
  resolvedErrors,
  activeErrors,
}: ErrorStatisticsProps) {
  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">
      <h2 className="mb-6 text-2xl font-bold text-[#3D348B]">
        Error Statistics
      </h2>

      <div className="space-y-5">

        <div className="flex justify-between">
          <span>Total Errors</span>
          <span className="font-bold">
            {totalErrors}
          </span>
        </div>

        <div className="flex justify-between">
          <span>Resolved</span>
          <span className="font-bold text-green-600">
            {resolvedErrors}
          </span>
        </div>

        <div className="flex justify-between">
          <span>Active</span>
          <span className="font-bold text-red-600">
            {activeErrors}
          </span>
        </div>

      </div>
    </div>
  );
}