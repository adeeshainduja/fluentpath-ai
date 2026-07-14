type ActionButtonsProps = {
  onSubmit: () => void;
  onRegenerate: () => void;
  onComplete: () => void;
  loading?: boolean;
};

export default function ActionButtons({
  onSubmit,
  onRegenerate,
  onComplete,
  loading = false,
}: ActionButtonsProps) {
  return (
    <div className="flex flex-wrap gap-4 justify-end">

      <button
        onClick={onRegenerate}
        disabled={loading}
        className="rounded-xl border border-[#3D348B] px-6 py-3 font-semibold text-[#3D348B] transition hover:bg-[#3D348B] hover:text-white disabled:opacity-50"
      >
        🔄 Regenerate
      </button>

      <button
        onClick={onComplete}
        disabled={loading}
        className="rounded-xl bg-green-600 px-6 py-3 font-semibold text-white transition hover:bg-green-700 disabled:opacity-50"
      >
        ✓ Mark Complete
      </button>

      <button
        onClick={onSubmit}
        disabled={loading}
        className="rounded-xl bg-[#3D348B] px-8 py-3 font-semibold text-white transition hover:bg-[#2c246a] disabled:opacity-50"
      >
        {loading ? "Submitting..." : "Submit Answer"}
      </button>

    </div>
  );
}