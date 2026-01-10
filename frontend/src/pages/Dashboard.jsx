import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';

export default function Dashboard() {
  const [stats, setStats] = useState({ count: 0, total: 0, successRate: 0 });
  const [recent, setRecent] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get('http://localhost:8000/api/v1/payments', {
          headers: { 'X-Api-Key': 'key_test_abc123', 'X-Api-Secret': 'secret_test_xyz789' }
        });
        const payments = Array.isArray(res.data) ? res.data : [];
        const successPay = payments.filter(p => p.status === 'success');
        const totalAmount = successPay.reduce((sum, p) => sum + (p.amount || 0), 0);

        setStats({
          count: payments.length,
          total: totalAmount,
          successRate: payments.length ? Math.round((successPay.length / payments.length) * 100) : 0
        });

        // recent transactions (most recent first)
        const recentSorted = payments.slice().sort((a, b) => new Date(b.created_at) - new Date(a.created_at)).slice(0, 6);
        setRecent(recentSorted);
        setLoading(false);
      } catch (err) { console.error(err); }
    };
    fetchData();
  }, []);

  const navigate = useNavigate();

  const handleLogout = () => {
    try { localStorage.removeItem('isLoggedIn'); } catch (e) {}
    navigate('/login');
  };

  return (
    <div className="main-content" data-test-id="dashboard">
      <div className="page-header" style={{marginBottom: 12}}>
        <h2 className="page-title" style={{margin: 0}}>Merchant Dashboard</h2>
        <div>
          <button className="logout-btn" onClick={handleLogout}>Logout</button>
        </div>
      </div>

      <nav className="page-nav" style={{ marginBottom: '18px' }}>
        <Link to="/dashboard" style={{ marginRight: '20px', fontWeight: 'bold' }}>Overview</Link>
        <Link to="/dashboard/transactions">Transactions</Link>
      </nav>

      {/* Compact hero to improve post-login appearance */}
      <div className="dashboard-hero">
        <div className="hero-left-compact">
          <div className="hero-logo">MG</div>
          <div className="hero-copy">
            <div className="hero-title">Merchant Dashboard</div>
            <div className="hero-sub">Key metrics at a glance</div>
          </div>
        </div>

        <div className="hero-kpis">
          <div className="hero-kpi">
            <div className="label">Total volume (success)</div>
            <div className="value">₹{(stats.total / 100).toFixed(2)}</div>
          </div>

          <div className="hero-kpi">
            <div className="label">Transactions</div>
            <div className="value">{stats.count}</div>
          </div>

          <div className="hero-kpi">
            <div className="label">Success rate</div>
            <div className="value" style={{ color: 'var(--success)' }}>{stats.successRate}%</div>
          </div>
        </div>

        <div className="hero-cta">
          <Link to="/dashboard/transactions" className="btn-primary">View Transactions</Link>
        </div>
      </div>

      <div className="card creds-box" data-test-id="api-credentials">
        <h3 style={{margin: 0}}>API Credentials</h3>
        <div><strong>Key: </strong><span data-test-id="api-key">key_test_abc123</span></div>
        <div><strong>Secret: </strong><span data-test-id="api-secret">secret_test_xyz789</span></div>
      </div>
      <div data-test-id="stats-container" className="stats-grid">
        <div className="stat-card">
          <div className="stat-meta">
            <div className="stat-label">Total Transactions</div>
            <div className="stat-value" data-test-id="total-transactions">{stats.count}</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-meta">
            <div className="stat-label">Total Volume</div>
            <div className="stat-value" data-test-id="total-amount">₹{(stats.total / 100).toFixed(2)}</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-meta">
            <div className="stat-label">Success Rate</div>
            <div className="stat-value" style={{color: 'var(--success)'}} data-test-id="success-rate">{stats.successRate}%</div>
          </div>
        </div>
      </div>

      

      <div className="card" style={{ marginTop: 8 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
          <h3 style={{ margin: 0 }}>Recent Transactions</h3>
          <Link to="/dashboard/transactions" className="muted small">View all</Link>
        </div>

        {loading ? <div className="muted">Loading recent transactions...</div> : (
          recent.length === 0 ? <div className="muted">No transactions yet.</div> : (
            <div className="tx-grid">
              {recent.map(tx => (
                <div className="tx-card" key={tx.id} data-payment-id={tx.id}>
                  <div className="tx-row">
                    <div>
                      <div className="tx-id">{tx.id}</div>
                      <div className="tx-meta">{tx.method || '—'} • {new Date(tx.created_at).toLocaleString()}</div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div className="tx-amount">₹{((tx.amount || 0) / 100).toFixed(2)}</div>
                      <div style={{ marginTop: 6 }}>
                        <span className={`tx-status ${tx.status === 'success' ? 'success' : tx.status === 'failed' ? 'failed' : 'pending'}`}>{tx.status}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )
        )}
      </div>
    </div>
  );
}

function Sparkline({ data, color = '#2563eb', width = 240, height = 48 }) {
  // build last 12 days series (amounts in rupees)
  const series = useMemo(() => {
    const days = 12;
    const map = {};
    (data || []).forEach(p => {
      if (!p || !p.created_at) return;
      const d = new Date(p.created_at);
      const key = d.toISOString().slice(0, 10);
      map[key] = (map[key] || 0) + ((p.amount || 0) / 100);
    });
    const out = [];
    for (let i = days - 1; i >= 0; i--) {
      const day = new Date();
      day.setDate(day.getDate() - i);
      const k = day.toISOString().slice(0, 10);
      out.push(map[k] || 0);
    }
    return out;
  }, [data]);

  const max = Math.max(...series, 1);
  const min = Math.min(...series);
  const points = series.map((v, i) => {
    const x = (i / (series.length - 1)) * width;
    const y = height - ((v - min) / (max - min || 1)) * height;
    return `${x},${y}`;
  }).join(' ');

  return (
    <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} preserveAspectRatio="none">
      <polyline fill="none" stroke={color} strokeWidth="2" points={points} strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}