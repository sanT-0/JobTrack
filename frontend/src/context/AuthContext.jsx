/**
 * AuthContext.jsx — Global authentication state via React Context.
 *
 * Why: Without context, every component that needs to know "is the user
 * logged in?" would need to read localStorage directly. Context gives us
 * one source of truth that all components subscribe to.
 *
 * What it provides:
 *   - user: the current user object (or null)
 *   - loading: true while checking auth on first load
 *   - login(token): saves token and loads user profile
 *   - logout(): clears token and user state
 */
import { createContext, useState, useEffect, useCallback } from "react";
import { authApi } from "../services/api";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true); // true until initial auth check done

  // On first render, check if there's a stored token and load the user
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setLoading(false);
      return;
    }
    authApi.me()
      .then((res) => setUser(res.data))
      .catch(() => localStorage.removeItem("token"))
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback(async (token) => {
    localStorage.setItem("token", token);
    const res = await authApi.me();
    setUser(res.data);
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("token");
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
