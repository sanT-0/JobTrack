/**
 * Navbar.jsx — Top navigation bar shown on all authenticated pages.
 */
import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  const initial = user?.name?.charAt(0).toUpperCase() || "U";

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <div className="navbar-brand">
          📋 <span>Job</span>Track
        </div>

        <div className="navbar-nav">
          <NavLink to="/dashboard" className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}>
            <span>Dashboard</span>
          </NavLink>
          <NavLink to="/applications" className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}>
            <span>Applications</span>
          </NavLink>
          <NavLink to="/profile" className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}>
            <span>Profile</span>
          </NavLink>
        </div>

        <div className="navbar-user">
          <span style={{ display: "none" }} id="user-name-display">{user?.name}</span>
          <div className="avatar" title={user?.name}>{initial}</div>
          <button className="btn btn-ghost btn-sm" onClick={handleLogout} id="logout-btn">
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}
