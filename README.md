---

# 🏗 Project Architecture Documentation

## Overview

This project follows **Clean Architecture principles** inspired by concepts from **Clean Architecture** by **Robert C. Martin**.

The main goals of this architecture:

* Separation of concerns
* Independent business logic (framework-agnostic)
* Easy testing
* Replaceable infrastructure (DB, messaging, etc.)
* Scalable and maintainable codebase

---

# 📂 Folder Structure Explanation

```
api/
config/
core/
cross_cutting/
tests/
```

---

# 1️⃣ `api/` – Presentation Layer (Interface Adapters)

This layer handles **external communication** (HTTP, REST, validation, serialization).

It depends on `core`, but `core` NEVER depends on `api`.

### Structure

```
api/
├── docs/              # API documentation (Swagger/OpenAPI configs)
├── middlewares/       # Custom HTTP middlewares
├── v1/                # Versioned API (v1)
│   ├── serializers/   # DTOs / request-response schemas
│   ├── views/         # Controllers / endpoints
├── validators/        # Request-level validation
```

### Responsibility

* Accept HTTP requests
* Validate input
* Call Application layer
* Return HTTP response

This layer may use:

* **Django Software Foundation**
* **Django**
* **FastAPI**

But switching frameworks should NOT affect business logic.

---

# 2️⃣ `config/` – Configuration Layer

```
config/
├── settings/
```

### Responsibility

* Environment settings
* App configuration
* Database configs
* External service configs

This layer contains:

* Dev / Prod configs
* Security settings
* Logging config

---

# 3️⃣ `core/` – Clean Architecture Core

This is the most important part.

It contains **Business Logic** and follows layered architecture:

```
core/
├── application/
├── domain/
└── infrastructure/
```

---

## 🧠 3.1 `domain/` – Enterprise Business Rules

Pure business logic.

No framework.
No database.
No Django/FastAPI imports.

```
domain/
├── order/
└── user/
```

### Contains

* Entities
* Value Objects
* Domain Rules
* Domain Exceptions

Example:

* `User`
* `Order`
* `Email`
* Business validation logic

👉 This is the most stable layer.

---

## ⚙ 3.2 `application/` – Use Cases Layer

This layer orchestrates business logic.

```
application/
├── interfaces/
├── order/
└── user/
```

### Contains

* Use Cases (CreateUser, CreateOrder)
* DTOs
* Interfaces (Repository contracts)
* Application services

Example:

```python
class CreateUserUseCase:
    def execute(self, data):
        ...
```

### Important Rule

Application depends on:

* Domain ✔
* Interfaces ✔

But NOT on:

* Database
* Django ORM
* External APIs

---

## 🏗 3.3 `infrastructure/` – External Implementations

This layer implements technical details.

```
infrastructure/
├── db/
│   ├── models/
│   └── repositories/
└── services/
```

### Contains

* ORM Models
* Repository implementations
* External APIs
* Email/SMS integrations
* Message broker implementations

This layer depends on:

* Application interfaces
* Frameworks
* Database drivers

Example:

* Django models
* PostgreSQL repository
* Redis cache client

---

# 4️⃣ `cross_cutting/` – Shared Concerns

Reusable modules used across layers.

```
shared/
├── auth/
├── caching/
├── error_handling/
├── logging/
├── messaging/
├── monitoring/
└── validation/
```

### Responsibility

* Authentication
* Logging
* Exception handling
* Caching
* Monitoring
* Messaging (RabbitMQ/Kafka)
* Common validators

These modules should not contain business logic.

---

# 5️⃣ `tests/` – Testing Strategy

```
tests/
├── e2e/
├── integration/
└── unit/
```

### Unit Tests

* Test domain and application logic
* No DB required

### Integration Tests

* Test infrastructure (DB, repositories)

### E2E Tests

* Full system testing
* API → DB → Response

---

# 🔄 Dependency Rule (Very Important)

Dependencies always point inward:

```
API → Application → Domain
Infrastructure → Application
```

Domain depends on NOTHING.

This ensures:

* Easy framework switching
* Easy DB switching
* High testability

---

# 🔥 Why This Architecture Is Powerful

✅ Business logic isolated
✅ Easy to test
✅ Scalable for microservices
✅ Replaceable infrastructure
✅ Framework-independent core

---

# 🎯 When To Use This Architecture

Use this when:

* Large project
* Long-term maintenance required
* Multiple developers
* Microservice-ready system
* Complex domain logic

For small CRUD apps, this might be overkill.

---

# 📌 Summary

| Layer          | Responsibility  | Depends On  |
| -------------- | --------------- | ----------- |
| API            | HTTP handling   | Application |
| Application    | Use cases       | Domain      |
| Domain         | Business rules  | Nothing     |
| Infrastructure | DB / External   | Application |
| Cross-cutting  | Shared concerns | All layers  |
| Tests          | Testing         | All layers  |

---
