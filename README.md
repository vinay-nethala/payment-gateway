# Payment Gateway

A full-stack payment gateway solution featuring a RESTful API, Merchant Dashboard, and Hosted Checkout Page. Built with Python (FastAPI), React, and PostgreSQL.

## 🚀 Features

* **Core API**: Order creation, payment processing, and status checks.
* **Payment Methods**: Support for UPI (VPA validation) and Credit Cards (Luhn algorithm & network detection).
* **Bank Simulation**: Realistic processing delays and random success/failure scenarios.
* **Merchant Dashboard**: Real-time transaction analytics and history.
* **Hosted Checkout**: Secure payment interface for customers.
* **Dockerized**: Full stack deployment with a single command.

## 🛠️ Tech Stack

* **Backend**: Python, FastAPI, SQLAlchemy
* **Database**: PostgreSQL 15
* **Frontend**: React, Vite
* **Containerization**: Docker, Docker Compose

## 🏁 Quick Start

1.  **Clone the repository**
    ```bash
    git clone <https://github.com/RAM-MEHER/payment-gateway>
    cd payment-gateway
    ```

2.  **Start the application**
    ```bash
    docker-compose up -d --build
    ```

3.  **Access the services**
    * **API**: http://localhost:8000
    * **Dashboard**: http://localhost:3000 (Login: `test@example.com` / any password)
    * **Checkout**: http://localhost:3001

## 🧪 Testing the Flow

1.  **Log in to the Dashboard** at `http://localhost:3000`. Note the API Keys.
2.  **Create an Order** via API:
    ```bash
    curl -X POST "http://localhost:8000/api/v1/orders" \
         -H "X-Api-Key: key_test_abc123" \
         -H "X-Api-Secret: secret_test_xyz789" \
         -H "Content-Type: application/json" \
         -d '{"amount": 50000, "currency": "INR", "receipt": "demo_1"}'
    ```
3.  **Copy the Order ID** from the response (e.g., `order_xyz...`).
4.  **Open Checkout Page**: `http://localhost:3001/?order_id=order_xyz...`
5.  **Complete Payment** using a test card (e.g., `4242 4242 4242 4242`).
6.  **Verify** the transaction appears in the Dashboard.

## 📂 Project Structure

```text
payment-gateway/
├── docker-compose.yml              # Orchestration for DB, API, Dashboard, Checkout
├── .env.example                    # Environment variables template
├── README.md                       # Project documentation
├── backend/                        # Backend Service (Port 8000)
│   ├── Dockerfile                  # API Container definition
│   ├── requirements.txt            # Python dependencies
│   └── app/
│       ├── __init__.py
│       ├── main.py                 # Application entry point & CORS setup
│       ├── database.py             # SQLAlchemy DB connection & session
│       ├── models.py               # Database Models (Merchant, Order, Payment)
│       ├── schemas.py              # Pydantic Schemas for Request/Response
│       ├── auth.py                 # API Key authentication logic
│       ├── utils.py                # Validators (Luhn, VPA, Expiry)
│       └── routers/                # API Route Handlers
│           ├── __init__.py
│           ├── health.py           # Health checks
│           ├── test_routes.py      # Test merchant verification
│           ├── orders.py           # Order creation & retrieval
│           ├── payments.py         # Payment processing (Authenticated)
│           └── public.py           # Public endpoints for Checkout page
├── frontend/                       # Merchant Dashboard (Port 3000)
│   ├── Dockerfile                  # Dashboard Container definition
│   ├── vite.config.js              # Vite configuration
│   ├── package.json                # Node dependencies
│   ├── index.html                  # React Entry HTML
│   ├── public/                     # Static assets
│   └── src/
│       ├── main.jsx                # React Entry Point
│       ├── App.jsx                 # Routing (Login, Dashboard, Transactions)
│       ├── App.css                 # Global Styles & Theme
│       └── pages/
│           ├── Login.jsx           # Merchant Login Page
│           ├── Dashboard.jsx       # Analytics & Stats Page
│           └── Transactions.jsx    # Transaction History Table
└── checkout-page/                  # Customer Checkout UI (Port 3001)
    ├── Dockerfile                  # Checkout Container definition
    ├── vite.config.js              # Vite configuration
    ├── package.json                # Node dependencies
    ├── index.html                  # React Entry HTML
    ├── public/                     # Static assets
    └── src/
        ├── main.jsx                # React Entry Point
        ├── App.jsx                 # Payment Flow Logic & UI
        └── App.css                 # Checkout specific styles
```

## 🔌 API Documentation

The API runs on port `8000`. All protected endpoints require API Key authentication.

**Base URL:** `http://localhost:8000`

### 🛡️ Authentication
Protected endpoints require the following headers:
* `X-Api-Key`: `<your_public_key>`
* `X-Api-Secret`: `<your_secret_key>`

---

### 1. Health Check
Checks if the API service and Database are running correctly.

* **Endpoint:** `GET /health`
* **Access:** Public
* **Response:**
    ```json
    {
      "status": "healthy",
      "database": "connected",
      "timestamp": "2026-01-08T10:00:00Z"
    }
    ```

---

### 2. Orders (Merchant Operations)
These endpoints are used by the merchant server to manage payment orders.

#### Create Order
Creates a new payment order (ledger entry).

* **Endpoint:** `POST /api/v1/orders`
* **Access:** Protected (Requires Auth Headers)
* **Request Body:**
    ```json
    {
      "amount": 50000,          // Amount in paise (e.g., ₹500.00)
      "currency": "INR",
      "receipt": "receipt#123", // Merchant's internal reference
      "notes": {
        "customer_name": "Rahul",
        "email": "rahul@example.com"
      }
    }
    ```
* **Response (201 Created):**
    ```json
    {
      "id": "order_a1b2c3d4e5f6g7h8",
      "amount": 50000,
      "status": "created",
      "created_at": "2026-01-08T10:05:00Z"
    }
    ```

#### Get Order Details
Fetches the current status of a specific order.

* **Endpoint:** `GET /api/v1/orders/{order_id}`
* **Access:** Protected
* **Response:**
    ```json
    {
      "id": "order_a1b2c3d4e5f6g7h8",
      "amount": 50000,
      "status": "paid",
      "merchant_id": "550e8400-e29b-41d4-a716-446655440000"
    }
    ```

---

### 3. Payments (Server-to-Server)
These endpoints allow merchants to process payments directly via API (Server-to-Server) or view transaction history.

#### Create Payment (S2S)
Process a payment using UPI or Card details directly.

* **Endpoint:** `POST /api/v1/payments`
* **Access:** Protected
* **Request Body (UPI Example):**
    ```json
    {
      "order_id": "order_a1b2c3d4e5f6g7h8",
      "method": "upi",
      "vpa": "user@okicici"
    }
    ```
* **Request Body (Card Example):**
    ```json
    {
      "order_id": "order_a1b2c3d4e5f6g7h8",
      "method": "card",
      "card": {
        "number": "4242424242424242",
        "expiry_month": "12",
        "expiry_year": "2030",
        "cvv": "123",
        "holder_name": "Test User"
      }
    }
    ```
* **Response:**
    ```json
    {
      "id": "pay_x9y8z7...",
      "status": "processing", // Initial status
      "amount": 50000,
      "method": "upi"
    }
    ```

#### List All Payments
Fetches a list of all transactions for the Merchant Dashboard.

* **Endpoint:** `GET /api/v1/payments`
* **Access:** Protected
* **Response:**
    ```json
    [
      {
        "id": "pay_1",
        "amount": 50000,
        "status": "success",
        "created_at": "..."
      },
      {
        "id": "pay_2",
        "amount": 2500,
        "status": "failed",
        "created_at": "..."
      }
    ]
    ```

---

### 4. Public Checkout (Browser)
These endpoints are public and used by the Hosted Checkout Page. They do not require API Keys but must be linked to a valid Order ID.

#### Fetch Order for Checkout
Used by the UI to display the amount to the customer.

* **Endpoint:** `GET /api/v1/public/orders/{order_id}`
* **Access:** Public
* **Response:**
    ```json
    {
      "id": "order_a1b2...",
      "amount": 50000,
      "currency": "INR",
      "merchant_name": "Test Merchant"
    }
    ```

#### Process Public Payment
Used by the Checkout UI to submit payment details securely.

* **Endpoint:** `POST /api/v1/public/payments`
* **Access:** Public
* **Request Body:** Same as the "Create Payment (S2S)" body above.

#### Check Payment Status (Polling)
Used by the UI to poll for the final status (Success/Failed) after processing.

* **Endpoint:** `GET /api/v1/public/payments/{payment_id}`
* **Access:** Public
* **Response:**
    ```json
    {
      "id": "pay_x9y8...",
      "status": "success",
      "error_code": null
    }
    ```