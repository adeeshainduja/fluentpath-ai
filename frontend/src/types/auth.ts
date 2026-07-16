// ================================
// Authentication Types
// ================================

export interface RegisterRequest {
  full_name: string;
  email: string;
  password: string;
  confirm_password?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

// ================================
// User
// ================================

export interface User {
  id: number;
  full_name: string;
  email: string;
  profile_photo_url?: string | null;
  english_level: string;
  target_goal: string;
  daily_goal: number;
  role: string;
  is_active: boolean;
  created_at: string;
}

export interface ProfileUpdateRequest {
  full_name?: string;
  profile_photo_url?: string | null;
  english_level?: string;
  target_goal?: string;
  daily_goal?: number;
}

// ================================
// Authentication Response
// ================================

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

// ================================
// Auth Context
// ================================

export interface AuthContextType {
  user: User | null;

  token: string | null;

  loading: boolean;

  isAuthenticated: boolean;

  login: (
    email: string,
    password: string
  ) => Promise<void>;

  register: (
    full_name: string,
    email: string,
    password: string,
    confirmPassword?: string
  ) => Promise<void>;

  updateProfile: (
    data: ProfileUpdateRequest
  ) => Promise<void>;

  logout: () => void;

  refreshUser: () => Promise<void>;
}
