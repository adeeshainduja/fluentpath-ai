import {
  PenSquare,
  Mic,
  BookOpen,
  Headphones,
  Languages,
} from "lucide-react";

import { useNavigate } from "react-router-dom";

import RecommendedPractice from "../../components/practice/RecommendedPractice";
import { useRecommendation } from "../../hooks/useRecommendation";
import api from "../../api/axios";
import { useAuth } from "../../hooks/useAuth";

const practiceTypes = [
  {
    title: "Writing",
    description: "Improve grammar and writing.",
    icon: PenSquare,
    color: "bg-blue-100 text-blue-600",
  },
  {
    title: "Speaking",
    description: "Practice pronunciation.",
    icon: Mic,
    color: "bg-green-100 text-green-600",
  },
  {
    title: "Reading",
    description: "Improve comprehension.",
    icon: BookOpen,
    color: "bg-yellow-100 text-yellow-600",
  },
  {
    title: "Listening",
    description: "Train your listening skills.",
    icon: Headphones,
    color: "bg-purple-100 text-purple-600",
  },
  {
    title: "Vocabulary",
    description: "Learn new words daily.",
    icon: Languages,
    color: "bg-pink-100 text-pink-600",
  },
];

export default function Practice() {
  const navigate = useNavigate();
  const { user } = useAuth();

  const {
    data: recommendation,
    isLoading,
  } = useRecommendation();

  const startPractice = async (practiceType: string) => {
    if (practiceType === "Speaking") {
      navigate("/practice/speaking");
      return;
    }

    if (practiceType === "Reading") {
      navigate("/practice/reading");
      return;
    }

    if (practiceType === "Listening") {
      navigate("/practice/listening");
      return;
    }

    if (practiceType === "Vocabulary") {
      navigate("/practice/vocabulary");
      return;
    }

    if (!user) {
      navigate("/login");
      return;
    }

    try {
      const response = await api.post(
        `/practice-tasks/learners/${user.id}/generate`
      );

      navigate(`/practice/${response.data.id}`);
    } catch (error) {
      console.error(error);
      alert("Failed to generate practice.");
    }
  };

  return (
    <div className="space-y-8">

      {/* Page Header */}
      <div>
        <h1 className="text-4xl font-bold text-[#3D348B]">
          Practice
        </h1>

        <p className="text-gray-500 mt-2">
          Choose a practice activity to improve your English.
        </p>
      </div>

      {/* AI Recommendation */}
      {!isLoading && recommendation && (
        <RecommendedPractice
          id={0}
          title={recommendation.recommendedPractice}
          practiceType={recommendation.recommendedPractice.toLowerCase()}
          skill={recommendation.recommendedPractice}
          difficulty={recommendation.difficulty}
          estimatedMinutes={parseInt(recommendation.estimatedTime, 10) || 15}
        />
      )}

      {/* Practice Cards */}
      <div className="grid gap-8 md:grid-cols-2 xl:grid-cols-3">
        {practiceTypes.map((item) => {
          const Icon = item.icon;

          return (
            <div
              key={item.title}
              className="rounded-3xl bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
            >
              <div
                className={`mb-5 flex h-14 w-14 items-center justify-center rounded-2xl ${item.color}`}
              >
                <Icon size={28} />
              </div>

              <h2 className="text-xl font-bold text-[#3D348B]">
                {item.title}
              </h2>

              <p className="mt-3 text-gray-500">
                {item.description}
              </p>

              <button
                onClick={() => startPractice(item.title)}
                className="mt-6 w-full rounded-xl bg-[#3D348B] py-3 font-semibold text-white transition hover:bg-[#2d2770]"
              >
                Start Practice
              </button>
            </div>
          );
        })}
      </div>

    </div>
  );
}
