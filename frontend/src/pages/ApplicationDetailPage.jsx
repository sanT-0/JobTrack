/**
 * ApplicationDetailPage.jsx — View and edit a single application.
 *
 * URL: /applications/:id
 *      /applications/:id?edit=true  — opens directly in edit mode
 */
import { useState, useEffect } from "react";
import { useParams, useNavigate, useSearchParams, Link } from "react-router-dom";
import { applicationsApi, getErrorMessage } from "../services/api";
import ApplicationForm from "../components/applications/ApplicationForm";
import StatusBadge from "../components/common/StatusBadge";
import Modal from "../components/common/Modal";
import Spinner from "../components/common/Spinner";
import { formatDate, formatDateTime } from "../utils/helpers";

export default function ApplicationDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const editMode = searchParams.get("edit") === "true";

  const [app, setApp] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(editMode);
  const [isSaving, setIsSaving] = useState(false);
  const [showDelete, setShowDelete] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const res = await applicationsApi.getOne(id);
        setApp(res.data);
      } catch (err) {
        setError(getErrorMessage(err));
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  async function handleSave(payload) {
    setIsSaving(true);
    setError("");
    try {
      const res = await applicationsApi.update(id, payload);
      setApp(res.data);
      setIsEditing(false);
      setSuccessMsg("Application updated successfully.");
      setTimeout(() => setSuccessMsg(""), 3000);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setIsSaving(false);
    }
  }

  async function handleDelete() {
    setIsDeleting(true);
    try {
      await applicationsApi.delete(id);
      navigate("/applications");
    } catch (err) {
      setError(getErrorMessage(err));
      setIsDeleting(false);
    }
  }

  if (loading) return <Spinner center />;
  if (error && !app) return (
    <div className="empty-state">
      <div className="empty-icon">⚠️</div>
      <h3>Could not load application</h3>
      <p>{error}</p>
      <Link to="/applications" className="btn btn-secondary mt-2">← Back to Applications</Link>
    </div>
  );

  return (
    <div className="form-page">
      {/* Header */}
      <div className="page-header">
        <div>
          <h1>{app.company}</h1>
          <p>{app.position}</p>
        </div>
        <div style={{ display: "flex", gap: "0.75rem" }}>
          <Link to="/applications" className="btn btn-secondary">← Back</Link>
          {!isEditing && (
            <>
              <button className="btn btn-primary" onClick={() => setIsEditing(true)}>Edit</button>
              <button className="btn btn-danger" onClick={() => setShowDelete(true)}>Delete</button>
            </>
          )}
        </div>
      </div>

      {successMsg && <div className="alert alert-success mb-2">{successMsg}</div>}
      {error && <div className="alert alert-error mb-2">{error}</div>}

      {isEditing ? (
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.5rem" }}>
            <h3>Edit Application</h3>
            <button className="btn btn-ghost btn-sm" onClick={() => setIsEditing(false)}>✕ Cancel</button>
          </div>
          <ApplicationForm
            initialData={{
              ...app,
              applied_date: app.applied_date || "",
              interview_date: app.interview_date || "",
              job_url: app.job_url || "",
              notes: app.notes || "",
              location: app.location || "",
              job_type: app.job_type || "",
            }}
            onSubmit={handleSave}
            isLoading={isSaving}
            submitLabel="Save Changes"
          />
        </div>
      ) : (
        <div className="card">
          {/* Status row */}
          <div style={{ display: "flex", gap: "0.75rem", alignItems: "center", marginBottom: "1.5rem" }}>
            <StatusBadge status={app.status} />
            {app.job_type && <span className="badge" style={{ background: "var(--bg-hover)", border: "1px solid var(--border)", color: "var(--text-secondary)" }}>{app.job_type}</span>}
          </div>

          <div className="detail-grid">
            <div className="detail-item"><label>Company</label><p>{app.company}</p></div>
            <div className="detail-item"><label>Position</label><p>{app.position}</p></div>
            <div className="detail-item"><label>Location</label><p>{app.location || "—"}</p></div>
            <div className="detail-item"><label>Status</label><p><StatusBadge status={app.status} /></p></div>
            <div className="detail-item"><label>Applied Date</label><p>{formatDate(app.applied_date)}</p></div>
            <div className="detail-item"><label>Interview Date</label><p>{formatDateTime(app.interview_date)}</p></div>
            <div className="detail-item">
              <label>Job URL</label>
              <p>
                {app.job_url
                  ? <a href={app.job_url} target="_blank" rel="noopener noreferrer" id="job-url-link">Open Job Listing ↗</a>
                  : "—"}
              </p>
            </div>
            <div className="detail-item"><label>Created</label><p>{formatDateTime(app.created_at)}</p></div>
          </div>

          {app.notes && (
            <>
              <div className="divider" />
              <div className="detail-item">
                <label>Notes</label>
                <p style={{ whiteSpace: "pre-wrap", marginTop: "0.5rem", color: "var(--text-primary)" }}>{app.notes}</p>
              </div>
            </>
          )}

          <div className="divider" />
          <p style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
            Last updated: {formatDateTime(app.updated_at)}
          </p>
        </div>
      )}

      {showDelete && (
        <Modal
          title="Delete Application"
          message={`Are you sure you want to delete the application for ${app.position} at ${app.company}? This cannot be undone.`}
          confirmLabel="Delete"
          onConfirm={handleDelete}
          onCancel={() => setShowDelete(false)}
          isLoading={isDeleting}
        />
      )}
    </div>
  );
}
