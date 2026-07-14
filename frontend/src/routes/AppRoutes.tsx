import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import MainLayout from "../layouts/MainLayout";

import Dashboard from "../pages/Dashboard/Dashboard";
import PracticeDetails from "../pages/PracticeDetails/PracticeDetails";

export default function AppRouter() {
  return (
    <BrowserRouter>

      <Routes>

        <Route element={<MainLayout />}>

          <Route
            path="/"
            element={<Dashboard />}
          />
          <Route
              path="/practice/:id"
              element={<PracticeDetails />}
          />

        </Route>

      </Routes>

    </BrowserRouter>
  );
}