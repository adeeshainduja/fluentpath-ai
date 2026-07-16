import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import MainLayout from "../layouts/MainLayout";

import Dashboard from "../pages/Dashboard/Dashboard";
import Practice from "../pages/Practice/Practice";
import PracticeDetails from "../pages/PracticeDetails/PracticeDetails";
import Analytics from "../pages/Analytics/Analytics";
import LearningPath from "../pages/LearningPath/LearningPath";
import AICoach from "../pages/AICoach/AICoach";
import Profile from "../pages/Profile/Profile";
import Settings from "../pages/Settings/Settings";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>

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
            path="/settings"
            element={<Settings />}
          />


        </Route>

      </Routes>
    </BrowserRouter>
  );
}
