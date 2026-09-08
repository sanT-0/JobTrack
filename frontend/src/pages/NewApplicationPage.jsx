/**
 * NewApplicationPage.jsx — Page for creating a new job application.
 */
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import ApplicationForm from "../components/applications/ApplicationForm";
import { applicationsApi, getErrorMessage } from "../services/api";

export default function NewApplicationPage() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState("");

  async function handleSubmit(payload) {
    setApiError("");
    setIsLoading(true);
    try {
      const res = await applicationsApi.create(payload);
      navigate(`/applications/${res.data.id}`);
    } catch (err) {
      setApiError(getErrorMessage(err));
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="form-page">
      <div className="page-header">
        <div>
          <h1>New Application</h1>
          <p>Track a new job you're applying to</p>
        </div>
        <Link to="/applications" className="btn btn-secondary">← Back</Link>
      </div>

      <div className="card">
        {apiError && <div className="alert alert-error mb-2">{apiError}</div>}
        <ApplicationForm
          onSubmit={handleSubmit}
          isLoading={isLoading}
          submitLabel="Create Application"
          initialData={{ applied_date: new Date().toISOString().split("T")[0] }}
        />
      </div>
    </div>
  );
}
