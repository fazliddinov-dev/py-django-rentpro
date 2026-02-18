

# 🏗️ Loyiha arxitekturasi

```
myproject/
├── config/         # Django core project config
├── core/           # Business logic (DDD + Clean Architecture)
│   ├── domain/     
│   ├── application/
│   └── infrastructure/
├── api/            # DRF delivery layer (views, serializers, urls)
├── cross_cutting/  # Logging, caching, monitoring, auth, validation
├── tests/
└── requirements/
```

---

## 1️⃣ `config/` — Django project settings

**Ma’qsad:** Django’ning `settings.py`, `urls.py`, `wsgi`/`asgi` fayllari.

**Qayerga yoziladi:**

* `config/settings/base.py` – umumiy settings (INSTALLED_APPS, MIDDLEWARE, DATABASES)
* `config/settings/development.py` – DEBUG=True, CORS, local DB
* `config/settings/production.py` – DEBUG=False, real DB, allowed hosts

**Nima yoziladi:**

* INSTALLED_APPS (core layer’ni Django app sifatida qo‘shish)
* MIDDLEWARE (admin ishlashi uchun Session, Auth, Messages)
* TEMPLATES (DjangoTemplates kerak bo‘lsa)
* DATABASES (initial sqlite3 yoki postgres config)

**Maslahat:** admin ishlashi uchun `SessionMiddleware`, `AuthMiddleware`, `MessageMiddleware` majburiy.

---

## 2️⃣ `core/` — Domain va biznes logika

**Ma’qsad:** Hamma “core” biznes qoidalar shu yerda, DRF yoki Django ORM dan mustaqil.

### a) `core/domain/` — Domain layer (DDD)

**Ma’qsad:** Business rules va domain knowledge.
**Nima yoziladi:**

* **entities.py** – asosiy entity’lar (`User`, `Order`)
* **value_objects.py** – kichik immutable obyektlar (`Email`, `Price`)
* **aggregates.py** – entity’larni birlashtiradigan aggregate root’lar
* **events.py** – domain event’lar (masalan `OrderCreated`)

**Qoidalar:** Bu layer **framework-agnostic**, ORM, DRF, HTTP bu layerga tegmasin.

---

### b) `core/application/` — Use Cases / Service layer

**Ma’qsad:** Application logic: request → response, domain bilan interfeys orqali ishlaydi.

**Qayerga yoziladi:**

* `user/use_cases.py` – `CreateUser`, `UpdateUser` kabi use-case’lar
* `user/dtos.py` – input/output data transfer object
* `interfaces/repositories.py` – abstract repository interface’lar (domain layer bilan bog‘lanish)
* `services.py` – domain service’lar, biznes qoidalarni implementatsiya qiladigan kod

**Qoidalar:**

* Bu layer DRF view yoki DB bilan bevosita ishlamaydi
* Repository interface orqali `infrastructure` bilan ishlaydi

---

### c) `core/infrastructure/` — Infrastructure layer

**Ma’qsad:** Real implementation: ORM, external services, DB access.

**Qayerga yoziladi:**

* `db/models/` – Django model fayllari
* `db/repositories/` – abstract interface’ni implementatsiya qiladi (`DjangoUserRepository`)
* `services/` – tashqi servislar (email, payment, SMS)

**Qoidalar:**

* Domain va Application layer’ga bog‘lanadi, lekin ulardan **business logic olmaydi**, faqat implementation

---

## 3️⃣ `api/` — Delivery / DRF layer

**Ma’qsad:** Django REST Framework orqali tashqi dunyoga API berish.

**Qayerga yoziladi:**

* `v1/serializers/` – domain data → JSON (DTO → serializer)
* `v1/views/` – DRF APIView yoki ViewSet, UseCase’ni chaqiradi
* `v1/urls.py` – API endpoint’lar

**Qoidalar:**

* View → UseCase (application layer) → Repository (infrastructure) → Domain
* Serializer faqat data transform qiladi, biznes qoidani yozmaydi

---

## 4️⃣ `cross_cutting/` — Shared concerns

**Ma’qsad:** Monitoring, logging, validation, caching, auth.

* `logging/logger.py` – structlog yoki standard logging
* `auth/authentication.py` – JWT auth, token verification
* `caching/cache_manager.py` – Redis yoki memcached wrapper
* `messaging/event_bus.py` – domain event bus
* `monitoring/metrics.py` – Prometheus metrics yoki custom
* `error_handling/exceptions.py` – custom exceptions
* `validation/validator.py` – shared validators

> Bu layer barcha qatlamlar tomonidan ishlatilishi mumkin.

---

## 5️⃣ `tests/` — Unit/Integration/E2E tests

**Ma’qsad:** Testlarni qatlam bo‘yicha ajratish

* `unit/` – domain + application layer tests
* `integration/` – infrastructure + DB tests
* `e2e/` – DRF API tests

---

## 6️⃣ Qatlamlar orasidagi flow

```text
[ DRF View ] 
       ↓
[ UseCase / Application Service ]
       ↓
[ Repository Interface ]
       ↓
[ Infrastructure Implementation (Django ORM / External Services) ]
       ↓
[ Domain Entity / Aggregate ]
```

* DRF View faqat request → UseCase → response
* UseCase domain bilan ishlaydi va repository’ni chaqiradi
* Domain toza biznes qoidalar, framework-agnostic
* Infrastructure data persist qilish yoki external servislar bilan ishlash

---

## 7️⃣ Oddiy misol (User create)

1️⃣ **Domain**: `User` entity

```python
# core/domain/user/entities.py
class User:
    def __init__(self, user_id: int, email: str):
        self.user_id = user_id
        self.email = email
```

2️⃣ **Application UseCase**

```python
# core/application/user/use_cases.py
from core.application.interfaces.repositories import UserRepository

class CreateUser:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def execute(self, email: str):
        user = User(user_id=0, email=email)
        self.repo.save(user)
        return user
```

3️⃣ **Infrastructure repository**

```python
# core/infrastructure/db/repositories/user_repository.py
from core.application.interfaces.repositories import UserRepository
from core.infrastructure.db.models.user_models import UserModel

class DjangoUserRepository(UserRepository):
    def save(self, user):
        UserModel.objects.create(email=user.email)
```

4️⃣ **DRF View**

```python
# api/v1/views/user_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from core.application.user.use_cases import CreateUser
from core.infrastructure.db.repositories.user_repository import DjangoUserRepository

class UserCreateView(APIView):
    def post(self, request):
        email = request.data["email"]
        use_case = CreateUser(DjangoUserRepository())
        user = use_case.execute(email)
        return Response({"id": user.user_id, "email": user.email})
```

> Bu misolda **qatlamlar aniq ajratilgan**, unit test yozish oson.

---