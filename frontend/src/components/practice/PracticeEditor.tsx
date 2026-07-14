import { useMemo } from "react";

interface Props {
  value: string;
  onChange: (value: string) => void;
}

export default function PracticeEditor({
  value,
  onChange,
}: Props) {

  const words = useMemo(() => {
    return value.trim()
      ? value.trim().split(/\s+/).length
      : 0;
  }, [value]);

  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">

      <h2 className="text-xl font-bold text-[#3D348B] mb-5">
        Your Answer
      </h2>

      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Write your answer here..."
        className="w-full h-72 rounded-xl border p-4 resize-none focus:outline-none focus:ring-2 focus:ring-[#3D348B]"
      />

      <div className="mt-4 flex justify-between text-sm text-gray-500">
        <span>Words: {words}</span>

        <span>Characters: {value.length}</span>
      </div>

    </div>
  );
}