/**
 * AuthLayout.jsx — Wrapper for login/register pages.
 * Redirects to dashboard if already authenticated.
 */
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import Spinner from "../components/common/Spinner";

export default function AuthLayout() {
  const { user, loading } = useAuth();

  if (loading) return <Spinner size="lg" center />;
  if (user) return <Navigate to="/dashboard" replace />;

  return (
    <div className="auth-layout">
      <Outlet />
    </div>
  );
}
