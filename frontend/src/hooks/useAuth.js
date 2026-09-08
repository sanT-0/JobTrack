/**
 * useAuth.js — Custom hook for consuming AuthContext.
 * Throws if used outside <AuthProvider> to catch mistakes early.
 */
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
