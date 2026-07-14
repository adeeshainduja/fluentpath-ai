import { useParams } from "react-router-dom";
import { usePractice } from "../../hooks/usePractice";

export default function PracticeDetail() {
  const { id } = useParams();

  const {
    data,
    loading,
    error,
  } = usePractice(Number(id));

  if (loading) return <h1>Loading...</h1>;

  if (error) return <h1>Error loading practice.</h1>;

  return (
    <div className="space-y-8">
      <h1 className="text-4xl font-bold text-[#3D348B]">
        Practice Details
      </h1>

      <div className="rounded-3xl bg-white p-8 shadow-sm">
        <h2 className="text-2xl font-bold">
          {data.title}
        </h2>

        <p className="mt-4">
          Skill:
          <strong> {data.target_skill}</strong>
        </p>

        <p>
          Practice Type:
          <strong> {data.practice_type}</strong>
        </p>

        <p>
          Difficulty:
          <strong> {data.difficulty}</strong>
        </p>

        <p>
          Status:
          <strong> {data.status}</strong>
        </p>
      </div>
    </div>
  );
}