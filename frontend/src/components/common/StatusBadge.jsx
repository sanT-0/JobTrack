/**
 * StatusBadge.jsx — Coloured badge for application status.
 */
import { statusToClass } from "../../utils/helpers";

export default function StatusBadge({ status }) {
  return (
    <span className={`badge badge-${statusToClass(status)}`}>
      {status}
    </span>
  );
}
