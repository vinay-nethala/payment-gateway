import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { CreditCard, Smartphone, CheckCircle, XCircle, Lock } from 'lucide-react';
import './App.css';

const API_URL = "http://localhost:8000/api/v1/public";

export default function App() {
  const [orderId, setOrderId] = useState(null);
  const [order, setOrder] = useState(null);
  const [method, setMethod] = useState(null); // 'upi' or 'card'
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("initial"); // initial, processing, success, failed
  
  // Form Data
  const [vpa, setVpa] = useState("");
  const [card, setCard] = useState({ number: "", expiry: "", cvv: "", name: "" });

  // 1. Get Order ID from URL on load
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const oid = params.get("order_id");
    if (oid) {
      setOrderId(oid);
      fetchOrder(oid);
    }
  }, []);

  const fetchOrder = async (id) => {
    try {
      const res = await axios.get(`${API_URL}/orders/${id}`);
      setOrder(res.data);
    } catch (err) {
      console.error("Order not found");
    }
  };

  // 2. Handle Payment
  const handlePay = async (e) => {
    e.preventDefault();
    setLoading(true);
    setStatus("processing");

    try {
      const payload = {
        order_id: orderId,
        method: method,
        ...(method === 'upi' ? { vpa } : {
          card: {
            number: card.number,
            expiry_month: card.expiry.split('/')[0],
            expiry_year: card.expiry.split('/')[1],
            cvv: card.cvv,
            holder_name: card.name
          }
        })
      };

      const res = await axios.post(`${API_URL}/payments`, payload);
      const payId = res.data.id;
      
      // 3. Poll for Status
      pollStatus(payId);
      
    } catch (err) {
      setStatus("failed");
      setLoading(false);
    }
  };

  const pollStatus = (payId) => {
    const interval = setInterval(async () => {
      try {
        const res = await axios.get(`${API_URL}/payments/${payId}`);
        if (res.data.status === 'success' || res.data.status === 'failed') {
          clearInterval(interval);
          setStatus(res.data.status);
          setLoading(false);
        }
      } catch (e) { clearInterval(interval); }
    }, 2000);
  };

  if (!order) return <div className="checkout-card">Loading Order...</div>;

  return (
    <div className="checkout-root">
      <div className="checkout-card" data-test-id="checkout-container">
        {/* HEADER */}
        <div className="checkout-header">
          <span className="label">Paying to Test Merchant</span>
          <div className="secure-label"><Lock size={12}/> Secure</div>
        </div>

        <div data-test-id="order-amount" className="amount">
          ₹{(order.amount / 100).toFixed(2)}
        </div>
      
      {/* SUCCESS STATE */}
      {status === 'success' && (
        <div data-test-id="success-state" className="state state-success">
          <CheckCircle size={64} color="#16a34a" />
          <h2>Payment Successful</h2>
          <p>Transaction completed successfully.</p>
        </div>
      )}

      {/* FAILED STATE */}
      {status === 'failed' && (
        <div data-test-id="error-state" className="state state-failed">
          <XCircle size={64} color="#ef4444" />
          <h2>Payment Failed</h2>
          <button onClick={() => setStatus('initial')} className="pay-btn pay-fail">Try Again</button>
        </div>
      )}

      {/* PROCESSING STATE */}
      {status === 'processing' && (
        <div data-test-id="processing-state" className="state state-processing">
          <div className="spinner"></div>
          <p>Processing Secure Payment...</p>
          <small className="label">Do not close this window</small>
        </div>
      )}

      {/* INITIAL FORM */}
      {status === 'initial' && (
        <>
          <div className="label" style={{marginBottom: '10px'}}>Select Payment Method</div>
          
          <button 
            data-test-id="method-upi" 
            className={`method-btn ${method === 'upi' ? 'active' : ''}`}
            onClick={() => setMethod('upi')}
          >
            <Smartphone size={18}/> UPI (Google Pay, PhonePe)
          </button>
          
          <button 
            data-test-id="method-card" 
            className={`method-btn ${method === 'card' ? 'active' : ''}`}
            onClick={() => setMethod('card')}
          >
            <CreditCard size={18}/> Credit / Debit Card
          </button>

          {method === 'upi' && (
            <form data-test-id="upi-form" onSubmit={handlePay} className="form-section">
              <input 
                data-test-id="vpa-input"
                className="input-field" 
                placeholder="username@bank" 
                value={vpa}
                onChange={e => setVpa(e.target.value)}
                required
              />
              <button data-test-id="pay-button" className="pay-btn">Pay Now</button>
            </form>
          )}

          {method === 'card' && (
            <form data-test-id="card-form" onSubmit={handlePay} className="form-section">
              <input 
                data-test-id="card-number-input"
                className="input-field" 
                placeholder="Card Number" 
                value={card.number}
                onChange={e => setCard({...card, number: e.target.value})}
                required
              />
              <div className="two-col">
                <input 
                  data-test-id="expiry-input"
                  className="input-field" 
                  placeholder="MM/YY" 
                  value={card.expiry}
                  onChange={e => setCard({...card, expiry: e.target.value})}
                  required
                />
                <input 
                  data-test-id="cvv-input"
                  className="input-field" 
                  placeholder="CVV" 
                  value={card.cvv}
                  onChange={e => setCard({...card, cvv: e.target.value})}
                  required
                />
              </div>
              <input 
                 data-test-id="cardholder-name-input"
                 className="input-field" 
                 placeholder="Cardholder Name"
                 value={card.name}
                 onChange={e => setCard({...card, name: e.target.value})}
                 required
               />
              <button data-test-id="pay-button" className="pay-btn">Pay Securely</button>
            </form>
          )}
        </>
      )}
      </div>
    </div>
  );
}