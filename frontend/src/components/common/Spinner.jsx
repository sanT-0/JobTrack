/**
 * Spinner.jsx — Loading spinner component.
 */
export default function Spinner({ size = "default", center = false }) {
  const cls = size === "lg" ? "spinner spinner-lg" : "spinner";
  if (center) {
    return <div className="loading-center"><div className={cls} /></div>;
  }
  return <div className={cls} />;
}
