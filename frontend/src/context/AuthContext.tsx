import {
  createContext,
  useEffect,
  useState,
} from "react";
import type { ReactNode } from "react";

import * as authApi from "../services/authApi";
import type {
  User,
  AuthContextType,
  ProfileUpdateRequest,
} from "../types/auth";

export const AuthContext =
  createContext<AuthContextType | null>(null);

interface Props {
  children: ReactNode;
}

export function AuthProvider({
  children,
}: Props) {
  const [user, setUser] =
    useState<User | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [token, setToken] = useState<string | null>(
    localStorage.getItem("access_token") ??
      localStorage.getItem("token")
  );

  useEffect(() => {
    if (token) {
      refreshUser();
    } else {
      setLoading(false);
    }
  }, []);

  async function refreshUser() {
    try {
      const user =
        await authApi.getCurrentUser();

      setUser(user);
    } catch {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("token");
      setToken(null);
      setUser(null);
    } finally {
      setLoading(false);
    }
  }

  async function login(
    email: string,
    password: string
  ) {
    const response =
      await authApi.login({
        email,
        password,
      });

    localStorage.setItem(
      "access_token",
      response.access_token
    );
    localStorage.setItem(
      "refresh_token",
      response.refresh_token
    );
    localStorage.removeItem("token");

    setToken(response.access_token);
    setUser(response.user);
  }

  async function register(
    full_name: string,
    email: string,
    password: string,
    confirmPassword?: string
  ) {
    await authApi.register({
      full_name,
      email,
      password,
      confirm_password:
        confirmPassword ?? password,
    });
  }

  async function updateProfile(
    data: ProfileUpdateRequest
  ) {
    const updatedUser =
      await authApi.updateProfile(data);

    setUser(updatedUser);
  }

  function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("token");

    setToken(null);
    setUser(null);
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,

        isAuthenticated:
          !!user,

        login,

        register,

        logout,

        refreshUser,

        updateProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
