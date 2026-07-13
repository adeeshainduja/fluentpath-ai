import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface TimelineItem {
  date: string;
  practice_count: number;
  average_score: number;
}

interface ProgressChartProps {
  timeline: TimelineItem[];
}

export default function ProgressChart({
  timeline,
}: ProgressChartProps) {
  const chartData = timeline.map((item) => ({
    day: new Date(item.date).toLocaleDateString("en-US", {
      weekday: "short",
    }),
    score: item.average_score,
  }));

  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">
      <div className="mb-6">
        <h2 className="text-xl font-bold text-[#3D348B]">
          Learning Progress
        </h2>

        <p className="text-sm text-gray-500">
          Average score over the last 7 days
        </p>
      </div>

      <ResponsiveContainer width="100%" height={320}>
        <AreaChart data={chartData}>
          <defs>
            <linearGradient
              id="score"
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

          <XAxis dataKey="day" />

          <YAxis domain={[0, 100]} />

          <Tooltip />

          <Area
            type="monotone"
            dataKey="score"
            stroke="#3D348B"
            strokeWidth={3}
            fill="url(#score)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}