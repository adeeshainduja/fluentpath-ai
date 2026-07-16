import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

const getAccessToken = () =>
  localStorage.getItem("access_token") ??
  localStorage.getItem("token");

api.interceptors.request.use((config) => {
  const token = getAccessToken();

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response?.status !== 401 ||
      originalRequest?._retry
    ) {
      return Promise.reject(error);
    }

    const refreshToken =
      localStorage.getItem("refresh_token");

    if (!refreshToken) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("token");
      return Promise.reject(error);
    }

    originalRequest._retry = true;

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/v1/auth/refresh",
        {
          refresh_token: refreshToken,
        }
      );

      localStorage.setItem(
        "access_token",
        response.data.access_token
      );
      localStorage.setItem(
        "refresh_token",
        response.data.refresh_token
      );
      localStorage.removeItem("token");

      originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`;

      return api(originalRequest);
    } catch (refreshError) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("token");
      return Promise.reject(refreshError);
    }
  }
);

export default api;
