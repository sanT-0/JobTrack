/**
 * AppLayout.jsx — Wrapper for all authenticated pages.
 * Redirects to login if not authenticated.
 */
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import Navbar from "../components/common/Navbar";
import Spinner from "../components/common/Spinner";

export default function AppLayout() {
  const { user, loading } = useAuth();

  if (loading) return <Spinner size="lg" center />;
  if (!user) return <Navigate to="/login" replace />;

  return (
    <div className="app-layout">
      <Navbar />
      <main className="page-content">
        <Outlet />
      </main>
    </div>
  );
}
