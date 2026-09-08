/**
 * RegisterPage.jsx — Registration form.
 */
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { authApi, getErrorMessage } from "../services/api";

export default function RegisterPage() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [form, setForm] = useState({ name: "", email: "", password: "", confirm: "" });
  const [errors, setErrors] = useState({});
  const [apiError, setApiError] = useState("");
  const [loading, setLoading] = useState(false);

  function validate() {
    const errs = {};
    if (!form.name.trim()) errs.name = "Name is required";
    if (!form.email) errs.email = "Email is required";
    else if (!/\S+@\S+\.\S+/.test(form.email)) errs.email = "Invalid email address";
    if (!form.password) errs.password = "Password is required";
    else if (form.password.length < 8) errs.password = "Password must be at least 8 characters";
    if (!form.confirm) errs.confirm = "Please confirm your password";
    else if (form.password !== form.confirm) errs.confirm = "Passwords do not match";
    return errs;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setApiError("");
    const errs = validate();
    if (Object.keys(errs).length) { setErrors(errs); return; }
    setErrors({});
    setLoading(true);
    try {
      const res = await authApi.register({ name: form.name.trim(), email: form.email, password: form.password });
      await login(res.data.access_token);
      navigate("/dashboard");
    } catch (err) {
      setApiError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }

  function handleChange(e) {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    setErrors((prev) => ({ ...prev, [e.target.name]: "" }));
  }

  return (
    <div className="auth-card">
      <div className="auth-logo">
        <h1>📋 <span style={{ color: "var(--accent)" }}>Job</span>Track</h1>
        <p>Create your account</p>
      </div>

      {apiError && (
        <div className="alert alert-error mb-2" role="alert">{apiError}</div>
      )}

      <form className="auth-form" onSubmit={handleSubmit} noValidate id="register-form">
        <div className="form-group">
          <label htmlFor="name">Full name</label>
          <input id="name" name="name" type="text" className="input" placeholder="Alex Johnson" value={form.name} onChange={handleChange} autoFocus />
          {errors.name && <span className="field-error">{errors.name}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="email">Email address</label>
          <input id="email" name="email" type="email" className="input" placeholder="you@example.com" value={form.email} onChange={handleChange} />
          {errors.email && <span className="field-error">{errors.email}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input id="password" name="password" type="password" className="input" placeholder="Min. 8 characters" value={form.password} onChange={handleChange} autoComplete="new-password" />
          {errors.password && <span className="field-error">{errors.password}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="confirm">Confirm password</label>
          <input id="confirm" name="confirm" type="password" className="input" placeholder="Repeat password" value={form.confirm} onChange={handleChange} autoComplete="new-password" />
          {errors.confirm && <span className="field-error">{errors.confirm}</span>}
        </div>

        <button id="register-submit" type="submit" className="btn btn-primary btn-full btn-lg" disabled={loading}>
          {loading ? "Creating account…" : "Create Account"}
        </button>
      </form>

      <p className="auth-footer">
        Already have an account? <Link to="/login">Sign in</Link>
      </p>
    </div>
  );
}
