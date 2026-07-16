import api from "../api/axios";

import type {
  LoginRequest,
  RegisterRequest,
  LoginResponse,
  ProfileUpdateRequest,
  User,
} from "../types/auth";

/**
 * Register a new user
 */
export async function register(
  data: RegisterRequest
): Promise<User> {
  const response = await api.post<User>(
    "/auth/register",
    data
  );

  return response.data;
}

/**
 * Login user
 */
export async function login(
  data: LoginRequest
): Promise<LoginResponse> {
  const response = await api.post<LoginResponse>(
    "/auth/login",
    data
  );

  return response.data;
}

/**
 * Get current authenticated user
 */
export async function getCurrentUser(): Promise<User> {
  const response = await api.get<User>(
    "/auth/me"
  );

  return response.data;
}

export async function refreshToken(
  refresh_token: string
): Promise<LoginResponse> {
  const response = await api.post<LoginResponse>(
    "/auth/refresh",
    {
      refresh_token,
    }
  );

  return response.data;
}

export async function updateProfile(
  data: ProfileUpdateRequest
): Promise<User> {
  const response = await api.put<User>(
    "/auth/profile",
    data
  );

  return response.data;
}

/**
 * Logout
 */
export async function logout(): Promise<void> {
  await api.post("/auth/logout");
}
