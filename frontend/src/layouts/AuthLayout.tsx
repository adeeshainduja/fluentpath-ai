import { Navigate, Outlet } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";

export default function AuthLayout() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#F5F6FC] text-[#3D348B]">
        <p className="text-lg font-semibold">Loading...</p>
      </div>
    );
  }

  if (isAuthenticated) {
    return <Navigate replace to="/" />;
  }

  return (
    <main className="min-h-screen bg-[#F5F6FC]">
      <div className="grid min-h-screen lg:grid-cols-[0.95fr_1.05fr]">
        <section className="hidden bg-[#3D348B] px-12 py-14 text-white lg:flex lg:flex-col lg:justify-between">
          <div>
            <h1 className="text-3xl font-bold">
              FluentPath AI
            </h1>
            <p className="mt-3 max-w-md text-white/75">
              Personal English coaching with practice, feedback, and progress that follows you.
            </p>
          </div>

          <div className="space-y-5">
            <div className="h-2 w-32 rounded-full bg-[#FFD166]" />
            <p className="max-w-lg text-4xl font-bold leading-tight">
              Build confident English communication one focused session at a time.
            </p>
          </div>
        </section>

        <section className="flex items-center justify-center p-6">
          <Outlet />
        </section>
      </div>
    </main>
  );
}
