import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { z } from "zod";

import { useAuth } from "../../hooks/useAuth";

const loginSchema = z.object({
  email: z.email("Enter a valid email address."),
  password: z.string().min(1, "Password is required."),
});

type LoginForm = z.infer<typeof loginSchema>;

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [formError, setFormError] = useState("");

  const {
    register,
    handleSubmit,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<LoginForm>({
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const onSubmit = async (values: LoginForm) => {
    setFormError("");
    const parsed = loginSchema.safeParse(values);

    if (!parsed.success) {
      parsed.error.issues.forEach((issue) => {
        const field = issue.path[0] as keyof LoginForm;
        setError(field, {
          message: issue.message,
        });
      });
      return;
    }

    try {
      await login(
        parsed.data.email,
        parsed.data.password
      );

      const redirectTo =
        (location.state as { from?: Location })?.from
          ?.pathname ?? "/";

      navigate(redirectTo, {
        replace: true,
      });
    } catch {
      setFormError("Invalid email or password.");
    }
  };

  return (
    <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-sm">
      <div>
        <p className="text-sm font-semibold uppercase tracking-wide text-[#3D348B]">
          Welcome back
        </p>
        <h1 className="mt-2 text-3xl font-bold text-[#3D348B]">
          Sign in
        </h1>
        <p className="mt-2 text-gray-500">
          Continue your English practice and review your progress.
        </p>
      </div>

      <form
        className="mt-8 space-y-5"
        onSubmit={handleSubmit(onSubmit)}
      >
        <label className="block space-y-2">
          <span className="text-sm font-semibold text-gray-600">
            Email
          </span>
          <input
            className="w-full rounded-xl border border-gray-200 bg-[#F5F6FC] px-4 py-3 outline-none transition focus:border-[#3D348B] focus:bg-white"
            type="email"
            {...register("email")}
          />
          {errors.email && (
            <span className="text-sm text-red-500">
              {errors.email.message}
            </span>
          )}
        </label>

        <label className="block space-y-2">
          <span className="text-sm font-semibold text-gray-600">
            Password
          </span>
          <input
            className="w-full rounded-xl border border-gray-200 bg-[#F5F6FC] px-4 py-3 outline-none transition focus:border-[#3D348B] focus:bg-white"
            type="password"
            {...register("password")}
          />
          {errors.password && (
            <span className="text-sm text-red-500">
              {errors.password.message}
            </span>
          )}
        </label>

        <div className="flex items-center justify-between text-sm">
          <Link
            className="font-semibold text-[#3D348B]"
            to="/forgot-password"
          >
            Forgot password?
          </Link>
        </div>

        {formError && (
          <p className="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-600">
            {formError}
          </p>
        )}

        <button
          className="w-full rounded-xl bg-[#3D348B] py-3 font-semibold text-white transition hover:bg-[#2d2770] disabled:opacity-60"
          disabled={isSubmitting}
          type="submit"
        >
          {isSubmitting ? "Signing in..." : "Sign in"}
        </button>
      </form>

      <p className="mt-6 text-center text-sm text-gray-500">
        New to FluentPath?{" "}
        <Link
          className="font-semibold text-[#3D348B]"
          to="/register"
        >
          Create an account
        </Link>
      </p>
    </div>
  );
}
