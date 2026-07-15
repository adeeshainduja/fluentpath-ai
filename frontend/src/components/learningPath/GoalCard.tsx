type Props = {
  current: number;
  target: number;
};

export default function GoalCard({
  current,
  target,
}: Props) {

  const progress = Math.min(
    (current / target) * 100,
    100
  );

  return (
    <div className="bg-white rounded-3xl shadow-sm border border-gray-100 p-6">

      <h2 className="text-xl font-bold text-[#3D348B] mb-5">
        Next Goal
      </h2>

      <div className="flex justify-between items-center mb-4">

        <div>

          <p className="text-gray-500">
            Current Score
          </p>

          <h1 className="text-4xl font-bold text-[#3D348B]">
            {current}%
          </h1>

        </div>

        <div className="text-right">

          <p className="text-gray-500">
            Target
          </p>

          <h1 className="text-4xl font-bold text-green-600">
            {target}%
          </h1>

        </div>

      </div>

      <div className="w-full h-4 bg-gray-200 rounded-full overflow-hidden">

        <div
          className="h-full rounded-full bg-[#3D348B]"
          style={{
            width: `${progress}%`,
          }}
        />

      </div>

      <p className="mt-4 text-gray-600">

        Only{" "}

        <span className="font-bold text-[#3D348B]">
          {target - current}%
        </span>

        {" "}remaining to reach your goal.

      </p>

    </div>
  );
}