/**
 * Modal.jsx — Reusable confirmation/dialog modal with overlay.
 */
export default function Modal({ title, message, onConfirm, onCancel, confirmLabel = "Confirm", confirmClass = "btn btn-danger", isLoading = false }) {
  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <h3>{title}</h3>
        <p>{message}</p>
        <div className="modal-actions">
          <button className="btn btn-secondary" onClick={onCancel} disabled={isLoading}>
            Cancel
          </button>
          <button className={confirmClass} onClick={onConfirm} disabled={isLoading}>
            {isLoading ? "Deleting…" : confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}
