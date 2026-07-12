import SummaryGrid from "../../components/dashboard/SummaryGrid";

export default function Dashboard() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-[#3D348B]">
          Dashboard
        </h1>

        <p className="text-gray-500">
          Welcome back! Here's your learning overview.
        </p>
      </div>

      <SummaryGrid />
    </div>
  );
}