import {
  Box,
  Grid,
  Stack,
  Typography,
} from "@mui/material";

import SummaryCard from "../../components/dashboard/SummaryCard";
import SummaryGrid from "../../components/dashboard/SummaryGrid";
import SkillRadar from "../../components/dashboard/SkillRadar";
import ProgressChart from "../../components/dashboard/ProgressChart";
import RecommendationCard from "../../components/dashboard/RecommendationCard";
import WeakSkills from "../../components/dashboard/WeakSkills";
import PracticeHistory from "../../components/dashboard/PracticeHistory";
import DailyMission from "../../components/dashboard/DailyMission";
import AchievementBadges from "../../components/dashboard/AchievementBadges";

export default function Analytics() {
  const summary = {
    average_score: 82,
    completed_tasks: 18,
    pending_tasks: 4,
    learning_trend: "Improving",
    recommended_skill: "Vocabulary",
    recommended_strategy: "Practice daily",
  };

  const skills = [
    {
      skill: "Grammar",
      average_score: 80,
    },
    {
      skill: "Vocabulary",
      average_score: 72,
    },
    {
      skill: "Fluency",
      average_score: 88,
    },
    {
      skill: "Pronunciation",
      average_score: 65,
    },
  ];

  const timeline = [
    {
      date: "Mon",
      average_score: 70,
    },
    {
      date: "Tue",
      average_score: 74,
    },
    {
      date: "Wed",
      average_score: 78,
    },
    {
      date: "Thu",
      average_score: 81,
    },
    {
      date: "Fri",
      average_score: 84,
    },
  ];

  const recommendation = {
    strategy: "Vocabulary Practice",
    priority_skill: "Vocabulary",
    reason: "Vocabulary score is lower than other skills.",
  };

  const weakSkills = [
    "Vocabulary",
    "Pronunciation",
  ];

  const missions = [
    {
      title: "Complete one vocabulary exercise",
      completed: false,
    },
    {
      title: "Practice speaking for 15 minutes",
      completed: true,
    },
  ];

  const history = [
    {
      title: "Business Email",
      score: 90,
      created_at: "2026-07-14",
    },
    {
      title: "Describe a Picture",
      score: 84,
      created_at: "2026-07-13",
    },
  ];

  return (
    <Box
      sx={{
        p: 4,
        backgroundColor: "#F8FAFC",
        minHeight: "100vh",
      }}
    >
      <Stack spacing={4}>
        <Box>
          <Typography
            variant="h4"
            fontWeight={700}
          >
            Analytics Dashboard
          </Typography>

          <Typography color="text.secondary">
            Track your English learning progress and AI insights.
          </Typography>
        </Box>

        <SummaryCard
          title="Overall Score"
          value={`${summary.average_score}%`}
        />

        <SummaryGrid summary={summary} />

        <Grid container spacing={3}>
          <Grid item xs={12} lg={6}>
            <SkillRadar skills={skills} />
          </Grid>

          <Grid item xs={12} lg={6}>
            <ProgressChart timeline={timeline} />
          </Grid>
        </Grid>

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <RecommendationCard
              recommendation={recommendation}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <WeakSkills skills={weakSkills} />
          </Grid>
        </Grid>

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <DailyMission missions={missions} />
          </Grid>

          <Grid item xs={12} md={6}>
            <AchievementBadges />
          </Grid>
        </Grid>

        <PracticeHistory history={history} />
      </Stack>
    </Box>
  );
}