import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

export default function Transactions() {
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    const fetchPayments = async () => {
      try {
        const res = await axios.get('http://localhost:8000/api/v1/payments', {
          headers: {
            'X-Api-Key': 'key_test_abc123',     // Hardcoded for MVP
            'X-Api-Secret': 'secret_test_xyz789'
          }
        });
        setPayments(Array.isArray(res.data) ? res.data : []);
      } catch (err) {
        console.error('Failed to fetch', err);
      } finally {
        setLoading(false);
      }
    };
    fetchPayments();
  }, []);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return payments.filter(p => {
      if (statusFilter !== 'all' && (p.status || '').toLowerCase() !== statusFilter) return false;
      if (!q) return true;
      return (p.id || '').toLowerCase().includes(q) || (p.method || '').toLowerCase().includes(q) || String((p.amount || 0) / 100).includes(q);
    }).sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  }, [payments, query, statusFilter]);

  return (
    <div className="transactions-container">
      <div style={{ marginBottom: 10 }}>
        <Link to="/dashboard">← Back to Dashboard</Link>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12, marginBottom: 8 }}>
        <h2 style={{ margin: 0 }}>Transaction History</h2>
        <div className="small muted">{payments.length} total</div>
      </div>

      <div className="tx-controls">
        <input className="tx-search" placeholder="Search by id, method, or amount" value={query} onChange={e => setQuery(e.target.value)} />
        <select className="tx-filter" value={statusFilter} onChange={e => setStatusFilter(e.target.value)}>
          <option value="all">All statuses</option>
          <option value="success">Success</option>
          <option value="failed">Failed</option>
          <option value="pending">Pending</option>
        </select>
      </div>

      {loading ? <div className="muted">Loading transactions...</div> : (
        filtered.length === 0 ? <div className="muted">No transactions match your filters.</div> : (
          <div className="tx-grid">
            {filtered.map(pay => (
              <div className="tx-card" key={pay.id} data-payment-id={pay.id}>
                <div className="tx-row">
                  <div>
                    <div className="tx-id">{pay.id}</div>
                    <div className="tx-meta">{pay.method || '—'} • {new Date(pay.created_at).toLocaleString()}</div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div className="tx-amount">₹{((pay.amount || 0) / 100).toFixed(2)}</div>
                    <div style={{ marginTop: 6 }}>
                      <span className={`tx-status ${pay.status === 'success' ? 'success' : pay.status === 'failed' ? 'failed' : 'pending'}`}>{pay.status}</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )
      )}
    </div>
  );
}