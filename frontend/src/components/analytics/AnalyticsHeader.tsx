import { Box, Typography } from "@mui/material";
import AnalyticsRoundedIcon from "@mui/icons-material/AnalyticsRounded";

export default function AnalyticsHeader() {
  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        mb: 4,
      }}
    >
      <Box>
        <Typography
          variant="h4"
          fontWeight={700}
        >
          Analytics Dashboard
        </Typography>

        <Typography
          variant="body1"
          color="text.secondary"
          sx={{ mt: 1 }}
        >
          Monitor your English learning progress with AI-powered insights.
        </Typography>
      </Box>

      <AnalyticsRoundedIcon
        sx={{
          fontSize: 52,
          color: "primary.main",
        }}
      />
    </Box>
  );
}