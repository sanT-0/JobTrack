/**
 * ProfilePage.jsx — View and update user profile (name, email, password).
 */
import { useState, useEffect } from "react";
import { useAuth } from "../hooks/useAuth";
import { usersApi, getErrorMessage } from "../services/api";
import { formatDate } from "../utils/helpers";
import Spinner from "../components/common/Spinner";

export default function ProfilePage() {
  const { user, login } = useAuth();
  const [profile, setProfile] = useState(null);
  const [name, setName] = useState("");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    async function loadProfile() {
      setIsLoading(true);
      try {
        const res = await usersApi.getProfile();
        setProfile(res.data);
        setName(res.data.name || "");
      } catch (err) {
        setErrorMessage(getErrorMessage(err));
      } finally {
        setIsLoading(false);
      }
    }
    loadProfile();
  }, []);

  async function handleUpdateProfile(e) {
    e.preventDefault();
    setErrorMessage("");
    setSuccessMessage("");

    if (!name.trim()) {
      setErrorMessage("Full name cannot be empty.");
      return;
    }

    if (newPassword) {
      if (newPassword.length < 6) {
        setErrorMessage("New password must be at least 6 characters long.");
        return;
      }
      if (newPassword !== confirmPassword) {
        setErrorMessage("New passwords do not match.");
        return;
      }
    }

    setIsSaving(true);
    try {
      const payload = { name: name.trim() };
      if (newPassword) {
        payload.new_password = newPassword;
        if (currentPassword) {
          payload.current_password = currentPassword;
        }
      }

      const res = await usersApi.updateProfile(payload);
      setProfile(res.data);
      setName(res.data.name);
      setNewPassword("");
      setConfirmPassword("");
      setCurrentPassword("");
      setSuccessMessage("Profile updated successfully!");

      // Update user in auth context if token still valid
      if (user) {
        login(localStorage.getItem("token"), res.data);
      }
    } catch (err) {
      setErrorMessage(getErrorMessage(err));
    } finally {
      setIsSaving(false);
    }
  }

  if (isLoading) {
    return <Spinner center text="Loading profile..." />;
  }

  const initials = (profile?.name || user?.name || "U")
    .split(" ")
    .map((n) => n[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  return (
    <div style={{ maxWidth: "680px", margin: "0 auto" }}>
      {/* Page Header */}
      <div className="page-header">
        <div>
          <h1>Account Profile</h1>
          <p>Manage your account settings and preferences</p>
        </div>
      </div>

      {successMessage && (
        <div className="alert alert-success mb-3" role="alert">
          ✓ {successMessage}
        </div>
      )}

      {errorMessage && (
        <div className="alert alert-error mb-3" role="alert">
          {errorMessage}
        </div>
      )}

      {/* Profile Card */}
      <div className="card mb-3">
        <div className="profile-header">
          <div className="profile-avatar">{initials}</div>
          <div className="profile-meta">
            <h2>{profile?.name || user?.name}</h2>
            <p>{profile?.email || user?.email}</p>
            <p style={{ fontSize: "0.8rem", color: "var(--text-muted)", marginTop: "0.2rem" }}>
              Member since: {formatDate(profile?.created_at)}
            </p>
          </div>
        </div>

        <div className="divider" />

        <form onSubmit={handleUpdateProfile}>
          <h3 className="mb-2" style={{ fontSize: "1.1rem" }}>Personal Information</h3>

          <div className="form-group mb-2">
            <label htmlFor="name">Full Name *</label>
            <input
              id="name"
              type="text"
              className="input"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Alex Johnson"
              required
            />
          </div>

          <div className="form-group mb-3">
            <label htmlFor="email">Email Address</label>
            <input
              id="email"
              type="email"
              className="input"
              value={profile?.email || ""}
              disabled
              style={{ opacity: 0.6, cursor: "not-allowed" }}
            />
            <span className="hint">Email address cannot be changed.</span>
          </div>

          <div className="divider" />

          <h3 className="mb-2" style={{ fontSize: "1.1rem" }}>Change Password</h3>
          <p className="mb-2" style={{ fontSize: "0.85rem" }}>
            Leave blank if you do not want to change your password.
          </p>

          <div className="form-group mb-2">
            <label htmlFor="currentPassword">Current Password</label>
            <input
              id="currentPassword"
              type="password"
              className="input"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              placeholder="••••••••"
              autoComplete="current-password"
            />
          </div>

          <div className="form-group mb-2">
            <label htmlFor="newPassword">New Password</label>
            <input
              id="newPassword"
              type="password"
              className="input"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="Minimum 6 characters"
              autoComplete="new-password"
            />
          </div>

          <div className="form-group mb-3">
            <label htmlFor="confirmPassword">Confirm New Password</label>
            <input
              id="confirmPassword"
              type="password"
              className="input"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Re-enter new password"
              autoComplete="new-password"
            />
          </div>

          <div className="flex" style={{ justifyContent: "flex-end" }}>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={isSaving}
            >
              {isSaving ? "Saving..." : "Save Changes"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
