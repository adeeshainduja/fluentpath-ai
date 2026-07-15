import { Clock, Sparkles, ArrowRight } from "lucide-react";
import { useNavigate } from "react-router-dom";

type Props = {
  id: number;
  title: string;
  practiceType: string;
  skill: string;
  difficulty: string;
  estimatedMinutes: number;
};

export default function RecommendedPractice({
  id,
  title,
  practiceType,
  skill,
  difficulty,
  estimatedMinutes,
}: Props) {
  const navigate = useNavigate();

  const handleContinue = () => {
    navigate(`/practice/${id}`);
  };

  return (
    <div className="bg-gradient-to-r from-[#3D348B] to-[#6C63FF] rounded-3xl shadow-lg text-white p-8">

      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <div className="w-14 h-14 rounded-2xl bg-white/20 flex items-center justify-center">
          <Sparkles size={28} />
        </div>

        <div>
          <h2 className="text-2xl font-bold">
            AI Recommended Practice
          </h2>

          <p className="text-white/80">
            Personalized lesson selected for today
          </p>
        </div>
      </div>

      {/* Lesson */}
      <h1 className="text-3xl font-bold mb-4">
        {title}
      </h1>

      {/* Tags */}
      <div className="flex flex-wrap gap-3 mb-6">

        <span className="bg-white/20 px-4 py-2 rounded-full text-sm">
          {practiceType}
        </span>

        <span className="bg-white/20 px-4 py-2 rounded-full text-sm">
          {skill}
        </span>

        <span className="bg-white/20 px-4 py-2 rounded-full text-sm">
          {difficulty}
        </span>

      </div>

      {/* Time */}
      <div className="flex items-center gap-2 mb-8">

        <Clock size={18} />

        <span>
          Estimated Time: {estimatedMinutes} minutes
        </span>

      </div>

      {/* Button */}
      <button
        onClick={handleContinue}
        className="bg-white text-[#3D348B] hover:bg-gray-100 transition px-6 py-3 rounded-xl font-semibold flex items-center gap-2"
      >
        Continue Practice

        <ArrowRight size={18} />
      </button>

    </div>
  );
}