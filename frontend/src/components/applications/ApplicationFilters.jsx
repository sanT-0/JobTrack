/**
 * ApplicationFilters.jsx — Search and filter bar for the applications list.
 */
const STATUSES = ["Applied", "Shortlisted", "Interview", "Offer", "Rejected", "Withdrawn"];
const JOB_TYPES = ["Full-Time", "Part-Time", "Contract", "Internship", "Remote", "Hybrid"];

export default function ApplicationFilters({ filters, onChange, onClear }) {
  function handleChange(e) {
    onChange({ ...filters, [e.target.name]: e.target.value, page: 1 });
  }

  const hasFilters = filters.search || filters.status || filters.job_type;

  return (
    <div className="filter-bar">
      <input
        id="filter-search"
        name="search"
        className="input"
        placeholder="🔍  Search company, position…"
        value={filters.search}
        onChange={handleChange}
      />
      <select id="filter-status" name="status" className="select" value={filters.status} onChange={handleChange}>
        <option value="">All Statuses</option>
        {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
      </select>
      <select id="filter-job-type" name="job_type" className="select" value={filters.job_type} onChange={handleChange}>
        <option value="">All Job Types</option>
        {JOB_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
      </select>
      {hasFilters && (
        <button id="filter-clear" className="btn btn-ghost btn-sm" onClick={onClear}>
          ✕ Clear
        </button>
      )}
    </div>
  );
}
