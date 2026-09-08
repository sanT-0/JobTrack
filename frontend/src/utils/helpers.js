/**
 * helpers.js — Shared utility functions used across the app.
 */

/** Format an ISO date string to a readable local date. */
export function formatDate(dateStr) {
  if (!dateStr) return "—";
  return new Date(dateStr).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

/** Format an ISO datetime string to date + time. */
export function formatDateTime(dateStr) {
  if (!dateStr) return "—";
  return new Date(dateStr).toLocaleString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

/** Map a status string to a CSS class suffix for the StatusBadge component. */
export function statusToClass(status) {
  const map = {
    Applied: "applied",
    Shortlisted: "shortlisted",
    Interview: "interview",
    Offer: "offer",
    Rejected: "rejected",
    Withdrawn: "withdrawn",
  };
  return map[status] || "applied";
}

/** Return today's date as YYYY-MM-DD for date input defaults. */
export function todayISO() {
  return new Date().toISOString().split("T")[0];
}

/** Truncate a string to maxLen chars. */
export function truncate(str, maxLen = 50) {
  if (!str) return "";
  return str.length > maxLen ? str.slice(0, maxLen) + "…" : str;
}
