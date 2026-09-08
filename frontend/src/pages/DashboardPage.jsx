/**
 * DashboardPage.jsx — Application overview, statistics, and upcoming interviews.
 */
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { dashboardApi, applicationsApi, getErrorMessage } from "../services/api";
import { formatDateTime, formatDate } from "../utils/helpers";
import Spinner from "../components/common/Spinner";
import StatusBadge from "../components/common/StatusBadge";

export default function DashboardPage() {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [interviews, setInterviews] = useState([]);
  const [recentApps, setRecentApps] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadDashboardData() {
      setIsLoading(true);
      setError("");
      try {
        const [statsRes, interviewsRes, appsRes] = await Promise.all([
          dashboardApi.getStats(),
          dashboardApi.getUpcomingInterviews(),
          applicationsApi.getAll({ limit: 5, sort_by: "created_at", order: "desc" }),
        ]);

        setStats(statsRes.data);
        setInterviews(interviewsRes.data || []);
        setRecentApps(appsRes.data?.items || []);
      } catch (err) {
        setError(getErrorMessage(err));
      } finally {
        setIsLoading(false);
      }
    }

    loadDashboardData();
  }, []);

  if (isLoading) {
    return <Spinner center text="Loading dashboard..." />;
  }

  const statCards = [
    { key: "total", label: "Total Applications", value: stats?.total ?? 0, className: "stat-total", color: "var(--accent)" },
    { key: "applied", label: "Applied", value: stats?.applied ?? 0, className: "stat-applied", color: "var(--status-applied)" },
    { key: "shortlisted", label: "Shortlisted", value: stats?.shortlisted ?? 0, className: "stat-shortlisted", color: "var(--status-shortlisted)" },
    { key: "interview", label: "Interviews", value: stats?.interview ?? 0, className: "stat-interview", color: "var(--status-interview)" },
    { key: "offer", label: "Offers", value: stats?.offer ?? 0, className: "stat-offer", color: "var(--status-offer)" },
    { key: "rejected", label: "Rejected", value: stats?.rejected ?? 0, className: "stat-rejected", color: "var(--status-rejected)" },
  ];

  return (
    <div>
      {/* Page Header */}
      <div className="page-header">
        <div>
          <h1>Dashboard</h1>
          <p>
            Welcome back, <strong style={{ color: "var(--text-primary)" }}>{user?.name}</strong>! Track your job applications and upcoming interviews.
          </p>
        </div>
        <div className="flex gap-1">
          <Link to="/applications/new" className="btn btn-primary">
            + New Application
          </Link>
        </div>
      </div>

      {error && (
        <div className="alert alert-error mb-3" role="alert">
          {error}
        </div>
      )}

      {/* Stats Grid */}
      <div className="stats-grid">
        {statCards.map((card) => (
          <Link
            key={card.key}
            to={card.key === "total" ? "/applications" : `/applications?status=${card.key.charAt(0).toUpperCase() + card.key.slice(1)}`}
            className={`stat-card ${card.className}`}
            style={{ textDecoration: "none" }}
          >
            <div className="stat-value" style={{ color: card.color }}>
              {card.value}
            </div>
            <div className="stat-label">{card.label}</div>
          </Link>
        ))}
      </div>

      {/* Split layout: Upcoming Interviews + Recent Applications */}
      <div className="detail-grid mb-3">
        {/* Upcoming Interviews */}
        <div className="card">
          <div className="flex items-center justify-between mb-2">
            <h3>Upcoming Interviews</h3>
            <span className="badge badge-interview">{interviews.length} Scheduled</span>
          </div>

          {interviews.length === 0 ? (
            <div className="empty-state" style={{ padding: "2rem 1rem" }}>
              <div className="empty-icon">📅</div>
              <h4>No Upcoming Interviews</h4>
              <p>When you schedule an interview in an application, it will appear here.</p>
            </div>
          ) : (
            <div className="interview-list">
              {interviews.map((app) => (
                <Link
                  key={app.id}
                  to={`/applications/${app.id}`}
                  className="interview-card"
                  style={{ textDecoration: "none" }}
                >
                  <div className="interview-info">
                    <h4 style={{ color: "var(--text-primary)" }}>{app.company}</h4>
                    <p>{app.position}</p>
                    {app.location && <p style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>📍 {app.location}</p>}
                  </div>
                  <div>
                    <div className="interview-date">
                      {formatDateTime(app.interview_date)}
                    </div>
                    <div style={{ marginTop: "0.25rem", textAlign: "right" }}>
                      <StatusBadge status={app.status} />
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>

        {/* Recent Applications */}
        <div className="card">
          <div className="flex items-center justify-between mb-2">
            <h3>Recent Applications</h3>
            <Link to="/applications" className="btn btn-ghost btn-sm">
              View All →
            </Link>
          </div>

          {recentApps.length === 0 ? (
            <div className="empty-state" style={{ padding: "2rem 1rem" }}>
              <div className="empty-icon">📝</div>
              <h4>No Applications Yet</h4>
              <p>Start your job tracking journey by adding your first application.</p>
              <Link to="/applications/new" className="btn btn-primary btn-sm mt-2">
                Add Application
              </Link>
            </div>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: "0.6rem" }}>
              {recentApps.map((app) => (
                <Link
                  key={app.id}
                  to={`/applications/${app.id}`}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    padding: "0.75rem 1rem",
                    background: "var(--bg-surface)",
                    borderRadius: "var(--radius-md)",
                    border: "1px solid var(--border)",
                    textDecoration: "none",
                    transition: "background var(--transition)",
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.background = "var(--bg-hover)")}
                  onMouseLeave={(e) => (e.currentTarget.style.background = "var(--bg-surface)")}
                >
                  <div>
                    <div style={{ fontWeight: 600, color: "var(--text-primary)" }}>{app.company}</div>
                    <div style={{ fontSize: "0.8rem", color: "var(--text-secondary)" }}>
                      {app.position} {app.job_type ? `• ${app.job_type}` : ""}
                    </div>
                  </div>
                  <div style={{ textAlign: "right" }}>
                    <StatusBadge status={app.status} />
                    <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "0.2rem" }}>
                      Applied: {formatDate(app.applied_date)}
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
