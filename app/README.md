# 💰 Finance Dashboard Backend System

## 📌 Overview

This project is a backend-driven finance dashboard system built using FastAPI. It allows users to manage financial records, perform analytics, and access data based on role-based permissions.

---

## 🚀 Features

### 👤 User Management

* Create, update, delete users
* Role-based access (Admin, Analyst, Viewer)
* User activation/deactivation

### 🔐 Authentication

* JWT-based login system
* Secure API access using Bearer token

### 💰 Financial Records

* Add income/expense records
* Update and delete records
* Filter by date, category, type

### 📊 Dashboard APIs

* Total income & expense
* Net balance
* Category-wise breakdown
* Monthly trends
* Recent transactions

---

## 🛠 Tech Stack

* Backend: FastAPI
* Database: SQLite
* ORM: SQLAlchemy
* Auth: JWT
* Frontend: HTML, CSS, JavaScript, Chart.js

---

## ⚙️ Setup Instructions

### 1. Clone Repository

git clone <your-repo-link>

### 2. Install Dependencies

pip install -r requirements.txt

### 3. Run Backend

uvicorn app.main:app --reload

### 4. Run Frontend

cd frontend
python -m http.server 5500

Open: http://127.0.0.1:5500/login.html

---

## 🔐 Authentication Flow

1. Login via `/users/login`
2. Copy access token
3. Use in headers:
   Authorization: Bearer <token>

---

## 📡 API Endpoints

### Users

* POST /users
* GET /users
* PUT /users/{id}
* DELETE /users/{id}

### Records

* POST /records
* GET /records

### Dashboard

* GET /dashboard/summary
* GET /dashboard/category
* GET /dashboard/recent
* GET /dashboard/monthly

---

## 📌 Assumptions

* Roles are predefined (admin, analyst, viewer)
* SQLite used for simplicity
* JWT used for authentication

---

## 👨‍💻 Author

Yash Arya
