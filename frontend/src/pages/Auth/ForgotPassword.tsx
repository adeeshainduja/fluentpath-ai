import { Link } from "react-router-dom";

export default function ForgotPassword() {
  return (
    <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-sm">
      <p className="text-sm font-semibold uppercase tracking-wide text-[#3D348B]">
        Account help
      </p>
      <h1 className="mt-2 text-3xl font-bold text-[#3D348B]">
        Forgot password
      </h1>
      <p className="mt-4 text-gray-500">
        Password reset email delivery is not configured yet. Contact your administrator to reset your FluentPath account password.
      </p>

      <Link
        className="mt-8 block rounded-xl bg-[#3D348B] py-3 text-center font-semibold text-white transition hover:bg-[#2d2770]"
        to="/login"
      >
        Back to sign in
      </Link>
    </div>
  );
}
