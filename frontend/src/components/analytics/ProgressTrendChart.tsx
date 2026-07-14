import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface ProgressTrendChartProps {
  data: {
    date: string;
    score: number;
  }[];
}

export default function ProgressTrendChart({
  data,
}: ProgressTrendChartProps) {
  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-[#3D348B]">
          Progress Trend
        </h2>

        <p className="text-gray-500">
          Your overall English score over time.
        </p>
      </div>

      <ResponsiveContainer
        width="100%"
        height={350}
      >
        <AreaChart data={data}>
          <defs>
            <linearGradient
              id="progressColor"
              x1="0"
              y1="0"
              x2="0"
              y2="1"
            >
              <stop
                offset="5%"
                stopColor="#4CB1FF"
                stopOpacity={0.8}
              />

              <stop
                offset="95%"
                stopColor="#4CB1FF"
                stopOpacity={0.05}
              />
            </linearGradient>
          </defs>

          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="date" />

          <YAxis domain={[0, 100]} />

          <Tooltip />

          <Area
            type="monotone"
            dataKey="score"
            stroke="#3D348B"
            strokeWidth={3}
            fill="url(#progressColor)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}