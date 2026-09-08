/**
 * api.js — Centralised Axios API service layer.
 *
 * Why: Scattering raw Axios calls across components makes the app hard to
 * maintain. One service file means one place to change base URLs, headers,
 * and error handling.
 *
 * Auth strategy: JWT is stored in localStorage. Every request through the
 * `api` instance automatically sends the token via an Axios interceptor.
 */
import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// ── Axios instance ─────────────────────────────────────────────────────────────
const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Redirect to login on 401 (expired/invalid token)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// ── Helper to extract a user-friendly error message ───────────────────────────
export function getErrorMessage(error) {
  if (error.response?.data?.detail) {
    const detail = error.response.data.detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail)) {
      return detail.map((e) => e.msg || String(e)).join(", ");
    }
  }
  return error.message || "An unexpected error occurred";
}

// ── Auth ───────────────────────────────────────────────────────────────────────
export const authApi = {
  register: (data) => api.post("/api/auth/register", data),
  login: (data) => api.post("/api/auth/login", data),
  me: () => api.get("/api/auth/me"),
};

// ── Applications ──────────────────────────────────────────────────────────────
export const applicationsApi = {
  getAll: (params) => api.get("/api/applications", { params }),
  getOne: (id) => api.get(`/api/applications/${id}`),
  create: (data) => api.post("/api/applications", data),
  update: (id, data) => api.put(`/api/applications/${id}`, data),
  delete: (id) => api.delete(`/api/applications/${id}`),
};

// ── Dashboard ─────────────────────────────────────────────────────────────────
export const dashboardApi = {
  getStats: () => api.get("/api/dashboard/stats"),
  getUpcomingInterviews: () => api.get("/api/dashboard/upcoming-interviews"),
};

// ── User profile ──────────────────────────────────────────────────────────────
export const usersApi = {
  getProfile: () => api.get("/api/users/me"),
  updateProfile: (data) => api.put("/api/users/me", data),
};

export default api;
