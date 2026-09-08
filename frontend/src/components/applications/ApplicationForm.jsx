/**
 * ApplicationForm.jsx — Reusable form for creating and editing applications.
 * Used by both NewApplicationPage and ApplicationDetailPage (edit mode).
 */
import { useState } from "react";

const STATUSES = ["Applied", "Shortlisted", "Interview", "Offer", "Rejected", "Withdrawn"];
const JOB_TYPES = ["Full-Time", "Part-Time", "Contract", "Internship", "Remote", "Hybrid"];

export default function ApplicationForm({ initialData = {}, onSubmit, isLoading, submitLabel = "Save Application" }) {
  const [form, setForm] = useState({
    company: "",
    position: "",
    location: "",
    job_type: "",
    status: "Applied",
    applied_date: "",
    interview_date: "",
    job_url: "",
    notes: "",
    ...initialData,
  });
  const [errors, setErrors] = useState({});

  function validate() {
    const errs = {};
    if (!form.company.trim()) errs.company = "Company is required";
    if (!form.position.trim()) errs.position = "Position is required";
    if (!form.status) errs.status = "Status is required";
    return errs;
  }

  function handleChange(e) {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    setErrors((prev) => ({ ...prev, [e.target.name]: "" }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length) { setErrors(errs); return; }

    // Build payload — exclude empty strings for optional fields
    const payload = {
      company: form.company.trim(),
      position: form.position.trim(),
      status: form.status,
      location: form.location.trim() || null,
      job_type: form.job_type || null,
      applied_date: form.applied_date || null,
      interview_date: form.interview_date ? new Date(form.interview_date).toISOString() : null,
      job_url: form.job_url.trim() || null,
      notes: form.notes.trim() || null,
    };
    onSubmit(payload);
  }

  return (
    <form onSubmit={handleSubmit} noValidate id="application-form">
      <div className="form-grid">
        {/* Company */}
        <div className="form-group">
          <label htmlFor="company">Company <span style={{ color: "var(--danger)" }}>*</span></label>
          <input id="company" name="company" className="input" placeholder="e.g. Google" value={form.company} onChange={handleChange} />
          {errors.company && <span className="field-error">{errors.company}</span>}
        </div>

        {/* Position */}
        <div className="form-group">
          <label htmlFor="position">Position <span style={{ color: "var(--danger)" }}>*</span></label>
          <input id="position" name="position" className="input" placeholder="e.g. Software Engineer" value={form.position} onChange={handleChange} />
          {errors.position && <span className="field-error">{errors.position}</span>}
        </div>

        {/* Location */}
        <div className="form-group">
          <label htmlFor="location">Location</label>
          <input id="location" name="location" className="input" placeholder="e.g. Remote, New York" value={form.location} onChange={handleChange} />
        </div>

        {/* Job Type */}
        <div className="form-group">
          <label htmlFor="job_type">Job Type</label>
          <select id="job_type" name="job_type" className="select" value={form.job_type} onChange={handleChange}>
            <option value="">Select type…</option>
            {JOB_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
          </select>
        </div>

        {/* Status */}
        <div className="form-group">
          <label htmlFor="status">Status <span style={{ color: "var(--danger)" }}>*</span></label>
          <select id="status" name="status" className="select" value={form.status} onChange={handleChange}>
            {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
          {errors.status && <span className="field-error">{errors.status}</span>}
        </div>

        {/* Applied Date */}
        <div className="form-group">
          <label htmlFor="applied_date">Applied Date</label>
          <input id="applied_date" name="applied_date" type="date" className="input" value={form.applied_date || ""} onChange={handleChange} />
        </div>

        {/* Interview Date */}
        <div className="form-group">
          <label htmlFor="interview_date">Interview Date & Time</label>
          <input id="interview_date" name="interview_date" type="datetime-local" className="input"
            value={form.interview_date ? form.interview_date.slice(0, 16) : ""}
            onChange={handleChange} />
        </div>

        {/* Job URL */}
        <div className="form-group">
          <label htmlFor="job_url">Job URL</label>
          <input id="job_url" name="job_url" type="url" className="input" placeholder="https://..." value={form.job_url || ""} onChange={handleChange} />
        </div>

        {/* Notes */}
        <div className="form-group span-2">
          <label htmlFor="notes">Notes</label>
          <textarea id="notes" name="notes" className="textarea" placeholder="Add notes about this application…" value={form.notes || ""} onChange={handleChange} />
        </div>
      </div>

      <div className="mt-3" style={{ display: "flex", gap: "0.75rem", justifyContent: "flex-end" }}>
        <button type="submit" id="application-submit" className="btn btn-primary btn-lg" disabled={isLoading}>
          {isLoading ? "Saving…" : submitLabel}
        </button>
      </div>
    </form>
  );
}
