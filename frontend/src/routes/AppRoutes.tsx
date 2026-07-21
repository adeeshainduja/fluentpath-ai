import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import MainLayout from "../layouts/MainLayout";
import AuthLayout from "../layouts/AuthLayout";
import ProtectedRoute from "./ProtectedRoute";

import Login from "../pages/Auth/Login";
import Register from "../pages/Auth/Register";
import ForgotPassword from "../pages/Auth/ForgotPassword";
import Dashboard from "../pages/Dashboard/Dashboard";
import Practice from "../pages/Practice/Practice";
import SpeakingPractice from "../pages/Practice/SpeakingPractice";
import PracticeDetails from "../pages/PracticeDetails/PracticeDetails";
import Analytics from "../pages/Analytics/Analytics";
import LearningPath from "../pages/LearningPath/LearningPath";
import AICoach from "../pages/AICoach/AICoach";
import Profile from "../pages/Profile/Profile";
import History from "../pages/History/History";
import HistoryDetail from "../pages/History/HistoryDetail";
import Settings from "../pages/Settings/Settings";
import ReadingPractice from "../pages/Reading/ReadingPractice";
import ListeningPractice from "../pages/Listening/ListeningPractice";
import VocabularyPractice from "../pages/Vocabulary/VocabularyPractice";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AuthLayout />}>
          <Route
            path="/login"
            element={<Login />}
          />
          <Route
            path="/register"
            element={<Register />}
          />
          <Route
            path="/forgot-password"
            element={<ForgotPassword />}
          />
        </Route>

        <Route element={<ProtectedRoute />}>
          <Route element={<MainLayout />}>

          {/* Dashboard */}
          <Route
            path="/"
            element={<Dashboard />}
          />

          {/* Practice List */}
          <Route
            path="/practice"
            element={<Practice />}
          />

          <Route
            path="/practice/speaking"
            element={<SpeakingPractice />}
          />

          <Route
            path="/practice/reading"
            element={<ReadingPractice />}
          />

          <Route
            path="/practice/listening"
            element={<ListeningPractice />}
          />
          <Route
            path="/practice/vocabulary"
            element={<VocabularyPractice />}
          />

          {/* Practice Details */}
          <Route
            path="/practice/:id"
            element={<PracticeDetails />}
          />
          <Route
            path="/analytics"
            element={<Analytics />}
          />

          <Route
            path="/learning-path"
            element={<LearningPath />}
          />

          <Route
            path="/ai-coach"
            element={<AICoach />}
          />

          <Route
            path="/profile"
            element={<Profile />}
          />

          <Route
            path="/history"
            element={<History />}
          />
          <Route
            path="/history/:attemptId"
            element={<HistoryDetail />}
          />

          <Route
            path="/settings"
            element={<Settings />}
          />
          </Route>
        </Route>

      </Routes>
    </BrowserRouter>
  );
}
