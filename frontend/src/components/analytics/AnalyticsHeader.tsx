export default function AnalyticsHeader() {
  return (
    <div className="flex items-center justify-between">
      <div>
        <h1 className="text-4xl font-bold text-[#3D348B]">
          Analytics Dashboard
        </h1>

        <p className="mt-2 text-gray-500">
          Monitor your English learning progress with AI-powered insights.
        </p>
      </div>

      <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-[#3D348B] to-[#4CB1FF] shadow-lg">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-8 w-8 text-white"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M3 3v18h18M8 16V9m5 7V5m5 11v-4"
          />
        </svg>
      </div>
    </div>
  );
}