/**
 * ApplicationsPage.jsx — List of all applications with search, filter, pagination.
 */
import { useState, useEffect, useCallback } from "react";
import { Link, useNavigate } from "react-router-dom";
import { applicationsApi, getErrorMessage } from "../services/api";
import ApplicationFilters from "../components/applications/ApplicationFilters";
import StatusBadge from "../components/common/StatusBadge";
import Modal from "../components/common/Modal";
import Spinner from "../components/common/Spinner";
import { formatDate } from "../utils/helpers";

const DEFAULT_FILTERS = { search: "", status: "", job_type: "", page: 1, page_size: 10 };

export default function ApplicationsPage() {
  const navigate = useNavigate();
  const [data, setData] = useState({ items: [], total: 0, page: 1, total_pages: 1 });
  const [filters, setFilters] = useState(DEFAULT_FILTERS);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [deleteId, setDeleteId] = useState(null);
  const [deleting, setDeleting] = useState(false);

  const fetchApplications = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const params = {};
      if (filters.search) params.search = filters.search;
      if (filters.status) params.status = filters.status;
      if (filters.job_type) params.job_type = filters.job_type;
      params.page = filters.page;
      params.page_size = filters.page_size;
      const res = await applicationsApi.getAll(params);
      setData(res.data);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    const timer = setTimeout(fetchApplications, 300); // debounce search
    return () => clearTimeout(timer);
  }, [fetchApplications]);

  async function handleDelete() {
    if (!deleteId) return;
    setDeleting(true);
    try {
      await applicationsApi.delete(deleteId);
      setDeleteId(null);
      fetchApplications();
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setDeleting(false);
    }
  }

  function changePage(p) {
    setFilters((f) => ({ ...f, page: p }));
  }

  return (
    <div>
      {/* Header */}
      <div className="page-header">
        <div>
          <h1>Applications</h1>
          <p>{data.total} total application{data.total !== 1 ? "s" : ""}</p>
        </div>
        <Link to="/applications/new" className="btn btn-primary" id="add-application-btn">
          + Add Application
        </Link>
      </div>

      {/* Filters */}
      <ApplicationFilters
        filters={filters}
        onChange={setFilters}
        onClear={() => setFilters(DEFAULT_FILTERS)}
      />

      {error && <div className="alert alert-error mb-2">{error}</div>}

      {/* Table */}
      <div className="table-wrapper">
        {loading ? (
          <Spinner center />
        ) : data.items.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📂</div>
            <h3>No applications found</h3>
            <p>
              {filters.search || filters.status || filters.job_type
                ? "Try adjusting your filters."
                : "Get started by adding your first application."}
            </p>
            {!filters.search && !filters.status && !filters.job_type && (
              <Link to="/applications/new" className="btn btn-primary mt-2">+ Add Application</Link>
            )}
          </div>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Company / Position</th>
                <th>Location</th>
                <th>Status</th>
                <th>Applied</th>
                <th>Interview</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {data.items.map((app) => (
                <tr key={app.id}>
                  <td data-label="Company">
                    <div className="table-company">{app.company}</div>
                    <div className="table-position">{app.position}</div>
                  </td>
                  <td data-label="Location">{app.location || "—"}</td>
                  <td data-label="Status"><StatusBadge status={app.status} /></td>
                  <td data-label="Applied">{formatDate(app.applied_date)}</td>
                  <td data-label="Interview">{formatDate(app.interview_date)}</td>
                  <td data-label="Actions">
                    <div className="table-actions">
                      <button className="btn btn-ghost btn-sm" onClick={() => navigate(`/applications/${app.id}`)}>View</button>
                      <button className="btn btn-secondary btn-sm" onClick={() => navigate(`/applications/${app.id}?edit=true`)}>Edit</button>
                      <button className="btn btn-danger btn-sm" onClick={() => setDeleteId(app.id)}>Delete</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {/* Pagination */}
        {data.total_pages > 1 && (
          <div className="pagination">
            <span>Page {data.page} of {data.total_pages} ({data.total} results)</span>
            <div className="pagination-controls">
              <button className="btn btn-secondary btn-sm" disabled={data.page <= 1} onClick={() => changePage(data.page - 1)}>← Prev</button>
              <button className="btn btn-secondary btn-sm" disabled={data.page >= data.total_pages} onClick={() => changePage(data.page + 1)}>Next →</button>
            </div>
          </div>
        )}
      </div>

      {/* Delete confirmation modal */}
      {deleteId && (
        <Modal
          title="Delete Application"
          message="Are you sure you want to delete this application? This action cannot be undone."
          confirmLabel="Delete"
          onConfirm={handleDelete}
          onCancel={() => setDeleteId(null)}
          isLoading={deleting}
        />
      )}
    </div>
  );
}
