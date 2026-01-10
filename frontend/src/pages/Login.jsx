import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck } from 'lucide-react'; // Icon

export default function Login() {
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    // simple demo auth flag
    try { localStorage.setItem('isLoggedIn', '1'); } catch (e) {}
    navigate('/dashboard');
  };

  return (
    <div className="auth-container">
      <div className="card login-card" role="region" aria-labelledby="login-title">
        <div className="login-header">
          <div className="login-logo">
            <ShieldCheck size={32} color="#2563eb" />
          </div>
          <h2 id="login-title" style={{margin: 0}}>Merchant Portal</h2>
          <p className="login-subtitle">Welcome back — manage payments effortlessly</p>
        </div>

        <form data-test-id="login-form" onSubmit={handleLogin} className="input-group">
          <input 
            data-test-id="email-input" 
            type="email" 
            placeholder="name@company.com" 
            defaultValue="test@example.com"
            aria-label="email"
          />
          <input 
            data-test-id="password-input" 
            type="password" 
            placeholder="Password" 
            aria-label="password"
          />

          <div className="form-actions">
            <label className="remember">
              <input type="checkbox" defaultChecked /> Remember me
            </label>
            <a className="forgot" href="#">Forgot?</a>
          </div>

          <button data-test-id="login-button" className="btn-primary" type="submit">
            Sign In to Dashboard
          </button>
        </form>
      </div>
    </div>
  );
}