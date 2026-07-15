import LearningHeader from "../../components/learningPath/LearningHeader";
import RecommendationCard from "../../components/learningPath/RecommendationCard";
import ProgressOverview from "../../components/learningPath/ProgressOverview";
import LearningTimeline from "../../components/learningPath/LearningTimeline";
import CurrentLesson from "../../components/learningPath/CurrentLesson";
import GoalCard from "../../components/learningPath/GoalCard";
import CoachPanel from "../../components/learningPath/CoachPanel";
import StreakCard from "../../components/learningPath/StreakCard";
import BadgeSection from "../../components/learningPath/BadgeSection";

import { useLearningPath } from "../../hooks/useLearningPath";

export default function LearningPath() {
  const learnerId = 1;

  const {
    data,
    isLoading,
    error,
  } = useLearningPath(learnerId);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-[70vh]">
        <h1 className="text-xl font-semibold text-[#3D348B]">
          Loading Learning Path...
        </h1>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex items-center justify-center h-[70vh]">
        <h1 className="text-xl font-semibold text-red-500">
          Failed to load Learning Path.
        </h1>
      </div>
    );
  }

  return (
    <div className="space-y-8">

      {/* Header */}
      <LearningHeader />

      {/* AI Recommendation */}
      <RecommendationCard
        id={data.current_stage.id}
        title={data.current_stage.title}
        skill={data.current_stage.skill}
        difficulty={data.current_stage.difficulty}
        estimatedMinutes={data.current_stage.estimated_minutes}
        reason="Based on your latest learning progress and adaptive AI analysis, this lesson will help improve your weakest skill."
      />

      {/* Progress + AI Coach */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

        <div className="lg:col-span-2">
          <ProgressOverview
            progress={data.overall_progress}
          />
        </div>

        <CoachPanel
          message={data.coach_message}
        />

      </div>

      {/* Learning Timeline */}
      <LearningTimeline
        roadmap={data.roadmap}
      />

      {/* Lesson + Goal + Side Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

        {/* Left Side */}
        <div className="lg:col-span-2 space-y-8">

          <CurrentLesson
            lesson={data.current_stage}
          />

          <GoalCard
            current={data.overall_progress}
            target={80}
          />

        </div>

        {/* Right Side */}
        <div className="space-y-8">

          <StreakCard
            streak={data.streak}
          />

          <BadgeSection
            badges={data.badges}
          />

        </div>

      </div>

    </div>
  );
}