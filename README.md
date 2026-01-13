# 💳✨ PAYMENT GATEWAY SYSTEM ✨💳  
### (UPI & Credit / Debit Card Payments – Test Mode)

🚀 A **fully containerized Payment Gateway simulation** inspired by **Razorpay / Stripe**.  
This project demonstrates **real-world payment workflows** including order creation, secure payments, merchant dashboards, and transaction tracking — **without real money**.

---

## 🧠 WHAT THIS PROJECT DOES

✔ Creates orders via REST API  
✔ Accepts payments via **UPI** and **Cards**  
✔ Validates payments using industry rules  
✔ Shows transactions in a **Merchant Dashboard**  
✔ Runs fully using **Docker** (one command)  

---

## 🧩 SYSTEM COMPONENTS

| Component | URL |
|---------|-----|
| 🧠 API Server | http://localhost:8000 |
| 📊 Merchant Dashboard | http://localhost:3000 |(Login: test@example.com / any password
| 🛒 Checkout Page | http://localhost:3001 |
| 🗄 Database | PostgreSQL |
| 🐳 Deployment | Docker Compose |

---

## 🏗️ ARCHITECTURE OVERVIEW

```
Merchant / Client
        |
        v
Dashboard (3000)
        |
        v
API Server (8000)
        |
        v
PostgreSQL Database
        |
        v
Checkout Page (3001)
```

---

## 🛠️ TECHNOLOGIES USED

🖥 Backend      : REST API (FastAPI / similar)  
🎨 Frontend     : React  
🗄 Database     : PostgreSQL  
🔐 Security     : API Key + Secret  
🐳 Deployment   : Docker & Docker Compose  

---

## ⚙️ HOW TO RUN THE PROJECT

### ✅ PREREQUISITES
- Docker installed
- Docker Compose enabled

---

### ▶️ START ALL SERVICES (ONE COMMAND)

```bash
docker-compose up -d
```

✨ This command will:
- Start API server
- Start Dashboard
- Start Checkout page
- Start Database
- Seed test merchant automatically

NO manual setup needed ❌

---

## 🧪 TEST MERCHANT (AUTO-CREATED)

🔑 These credentials are **TEST MODE ONLY**

```
X-Api-Key     : key_test_abc123
X-Api-Secret  : secret_test_xyz789
```

📌 NOTE:
- Same for everyone
- Auto-seeded on startup
- Used for evaluation & testing

---

## 🔐 API AUTHENTICATION FORMAT

All API requests must include:

```
X-Api-Key: key_test_abc123
X-Api-Secret: secret_test_xyz789
Content-Type: application/json
```

---

## 🧾 STEP 1: CREATE ORDER (MANDATORY)

📍 Windows CMD / VS Code Terminal

```bash
curl -X POST http://localhost:8000/api/v1/orders -H "X-Api-Key: key_test_abc123" -H "X-Api-Secret: secret_test_xyz789" -H "Content-Type: application/json" -d "{\"amount\":50000,\"currency\":\"INR\",\"receipt\":\"demo_1\"}"
```

📥 RESPONSE EXAMPLE:

```json
{
  "id": "order_xxxxx",
  "status": "created",
  "amount": 50000,
  "currency": "INR"
}
```

📌 Save the **order_id** — required for payment

---

## 💳 STEP 2A: CREDIT / DEBIT CARD PAYMENT

### 🧪 TEST CARD DETAILS

```
Card Number : 4242 4242 4242 4242
Expiry      : 12 / 2026
CVV         : 123
holder name :Test User

```

### ▶️ API COMMAND

```bash
curl -X POST http://localhost:8000/api/v1/payments -H "X-Api-Key: key_test_abc123" -H "X-Api-Secret: secret_test_xyz789" -H "Content-Type: application/json" -d "{\"order_id\":\"order_xxxxx\",\"method\":\"card\",\"card\":{\"number\":\"4242424242424242\",\"expiry_month\":\"12\",\"expiry_year\":\"2026\",\"cvv\":\"123\",\"holder_name\":\"Test User\"}}"
```

### ✅ CARD VALIDATIONS
✔ Luhn Algorithm  
✔ Expiry Date Check  
✔ Card Network Detection  
✔ CVV Validation  
✔ Only last 4 digits stored  

---

## 📱 STEP 2B: UPI PAYMENT

### 🧪 TEST VPA

```
testuser@paytm
```

### ▶️ API COMMAND

```bash
curl -X POST http://localhost:8000/api/v1/payments -H "X-Api-Key: key_test_abc123" -H "X-Api-Secret: secret_test_xyz789" -H "Content-Type: application/json" -d "{\"order_id\":\"order_xxxxx\",\"method\":\"upi\",\"vpa\":\"testuser@paytm\"}"
```

### ✅ UPI VALIDATIONS
✔ VPA format check  
✔ Simulated bank response  

---

## 🔄 PAYMENT STATUS FLOW

```
created → processing → success / failed
```

📊 Simulated Success Rates:
- 💳 Cards : 95%
- 📱 UPI   : 90%

---

## 🛒 CHECKOUT PAGE (USER FLOW)

🌐 Open in browser:

```
http://localhost:3001/?order_id=order_xxxxx
```

🧭 Steps:
1. Order details displayed
2. Choose payment method
3. Enter details
4. Click **Pay**
5. View success / failure

---

## 📊 MERCHANT DASHBOARD

🌐 Open:

```
http://localhost:3000
```

📌 Dashboard Displays:
✔ API credentials  
✔ Orders summary  
✔ Successful payments  
✔ Failed payments  
✔ Transaction list  

---

## 🔒 SECURITY PRACTICES

🔐 API Key authentication  
🔐 No real payment gateway  
🔐 No CVV storage  
🔐 Card data masked  
🔐 Test mode only  

---

## 🗄 DATABASE STRUCTURE

Tables:
- merchants
- api_keys
- orders
- payments
- transactions

Relationships:
- Merchant → Orders
- Order → Payments
- Payment → Transaction

---

## 🧪 TEST MODE DISCLAIMER

⚠️ This is a **SIMULATION PROJECT**
- No real money
- No real banks
- Built for learning & evaluation

---

## 🎯 PROJECT USE CASES

🎓 Learning Payment Systems  
💼 Internship / Job Evaluation  
🧪 API Testing Practice  
🧱 System Design Demonstration  

---

## ✅ PROJECT IS COMPLETE WHEN

✔ Docker runs successfully  
✔ Orders can be created  
✔ Payments succeed  
✔ Dashboard updates  

---

✨ END OF DOCUMENT ✨
