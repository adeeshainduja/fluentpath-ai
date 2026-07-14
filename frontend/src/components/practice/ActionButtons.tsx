interface Props {
  onSubmit: () => void;
}

export default function ActionButtons({
  onSubmit,
}: Props) {
  return (
    <div className="flex gap-4 mt-6">

      <button className="rounded-xl border px-5 py-3">
        Save Draft
      </button>

      <button className="rounded-xl border px-5 py-3">
        Ask AI Hint
      </button>

      <button
        onClick={onSubmit}
        className="rounded-xl bg-[#3D348B] px-6 py-3 text-white"
      >
        Submit Answer
      </button>

    </div>
  );
}