import {
  Card,
  CardContent,
  LinearProgress,
  Stack,
  Typography,
} from "@mui/material";

interface OverallScoreCardProps {
  score: number;
}

export default function OverallScoreCard({
  score,
}: OverallScoreCardProps) {
  return (
    <Card
      elevation={2}
      sx={{
        borderRadius: 4,
      }}
    >
      <CardContent>
        <Stack spacing={2}>
          <Typography
            variant="h6"
            fontWeight={600}
          >
            Overall English Score
          </Typography>

          <Typography
            variant="h2"
            color="primary"
            fontWeight={700}
          >
            {score}
          </Typography>

          <LinearProgress
            variant="determinate"
            value={score}
            sx={{
              height: 10,
              borderRadius: 5,
            }}
          />

          <Typography
            variant="body2"
            color="text.secondary"
          >
            Your overall performance across all completed practice sessions.
          </Typography>
        </Stack>
      </CardContent>
    </Card>
  );
}