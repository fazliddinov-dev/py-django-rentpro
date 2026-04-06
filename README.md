# 🚀 Multi-Tenant SaaS Booking System

A production-ready backend system where multiple businesses (tenants) can manage services, accept bookings, and operate under a subscription model.

---

## 🧠 Overview

This project simulates a real-world SaaS platform used by businesses such as salons, gyms, and rental services.

Each business can:

* Register and create its own workspace
* Manage staff and customers
* Create and manage services
* Accept and control bookings
* Use the system through a subscription plan

The system is designed with **scalability, isolation, and production-grade architecture** in mind.

---

## 🏗 Architecture

### 🔑 Multi-Tenancy

Each company (tenant) has fully isolated data:

* Users belong to a company
* Services belong to a company
* Bookings belong to a company

```
Company → Users → Services → Bookings
```

---

### 🔐 Authentication & Roles

Custom `User` model with role-based access control:

* **Owner** – manages company and subscription
* **Staff** – manages services and bookings
* **Customer** – creates bookings

---

### 💳 Subscription System

* Businesses must subscribe to access the platform
* Plans define usage limits (staff, services, etc.)
* Subscription lifecycle:

  * Active
  * Expired
  * Cancelled

Access to core features is restricted based on subscription status.

---

### ⚡ Background Processing

Using **Celery + Redis** for asynchronous tasks:

* Subscription expiration checks
* Notifications (email/SMS ready)
* Non-blocking background jobs

---

### 🚀 Caching

Redis is used to improve performance:

* Cache frequently accessed data (e.g. services)
* Reduce database load

---

## ⚙️ Tech Stack

* **Backend:** Django, Django REST Framework
* **Database:** PostgreSQL
* **Cache & Queue:** Redis
* **Async Tasks:** Celery
* **Containerization:** Docker

---

## 📁 Project Structure

```
apps/
  user/
  subscription/
  booking/
  service/
  payment/

```

---

## 🔥 Key Features

* Multi-tenant architecture
* Role-based access control
* Subscription & plan management
* Booking system with conflict prevention
* Background job processing (Celery)
* Redis caching
* Service layer (clean architecture)

---

## 🧠 Architecture Decisions

* Used **tenant-based isolation (company_id)** for scalability and simplicity
* Implemented **service layer** to separate business logic from views
* Used **Celery** to avoid blocking HTTP requests
* Applied **database constraints & transactions** to prevent race conditions
* Designed **subscription-based access control** to simulate real SaaS systems

---

## 🚀 How to Run

### 1. Clone repository

```bash
git clone https://github.com/yourusername/saas-booking-system.git
cd saas-booking-system
```

---

### 2. Run with Docker

```bash
docker-compose up --build
```

---

### 3. Apply migrations

```bash
docker-compose exec web python manage.py migrate
```

---

### 4. Create superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

---

## 📬 API Endpoints (Examples)

```
POST   /auth/register/
POST   /auth/login/

GET    /plans/
POST   /subscriptions/subscribe/

POST   /services/
POST   /bookings/
```

---

## 🔒 Business Rules

* Users cannot access core features without an active subscription
* Expired subscriptions block service creation and bookings
* Booking conflicts are prevented using database constraints

---

## 💥 Why This Project Matters

This is not a simple CRUD application.

It demonstrates:

* Real SaaS architecture
* Multi-tenancy
* Async processing
* Clean code practices
* Production-ready backend design

---

## 🚀 Future Improvements

* Stripe integration for real payments
* WebSocket-based real-time notifications
* Advanced analytics dashboard
* Rate limiting and throttling
* Multi-language support

---

## 👨‍💻 Author

**Kamoliddin Fazliddinov**
Backend Developer (Python / Django)
