Ajoyib! Keling, men senga **sening Clean Architecture + DDD + DRF skeleton** bo‘yicha **barcha qatlamlar ishlatiladigan real misol**ni ko‘rsataman.

Bu misol **“Order yaratish API”** bo‘ladi, va har bir layer ishtirok etadi:

* **Domain**: `Order` entity, `OrderId` value object, `OrderCreated` event
* **Application**: `CreateOrderUseCase`, DTO
* **Infrastructure**: Django model, repository implementation, external service (fake payment)
* **API**: DRF view, serializer, URL
* **Cross-cutting**: Logging, validation

---

# 1️⃣ Domain layer

```python
# core/domain/order/entities.py
from core.domain.order.value_objects import OrderId, Price

class Order:
    def __init__(self, order_id: OrderId, user_id: int, price: Price):
        self.order_id = order_id
        self.user_id = user_id
        self.price = price
```

```python
# core/domain/order/value_objects.py
class OrderId:
    def __init__(self, id: int):
        self.id = id

class Price:
    def __init__(self, amount: float):
        if amount < 0:
            raise ValueError("Price cannot be negative")
        self.amount = amount
```

```python
# core/domain/order/events.py
class OrderCreated:
    def __init__(self, order_id: int):
        self.order_id = order_id
```

---

# 2️⃣ Application layer

```python
# core/application/order/dtos.py
from dataclasses import dataclass

@dataclass
class CreateOrderDTO:
    user_id: int
    amount: float
```

```python
# core/application/interfaces/repositories.py
from abc import ABC, abstractmethod
from core.domain.order.entities import Order

class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order):
        pass
```

```python
# core/application/order/use_cases.py
from core.application.interfaces.repositories import OrderRepository
from core.application.order.dtos import CreateOrderDTO
from core.domain.order.entities import Order
from core.domain.order.value_objects import OrderId, Price
from core.domain.order.events import OrderCreated

class CreateOrderUseCase:
    def __init__(self, order_repo: OrderRepository, logger=None):
        self.order_repo = order_repo
        self.logger = logger

    def execute(self, dto: CreateOrderDTO) -> OrderCreated:
        order_id = OrderId(id=0)  # real DB assign qiladi
        price = Price(amount=dto.amount)
        order = Order(order_id, dto.user_id, price)
        self.order_repo.save(order)
        if self.logger:
            self.logger.info(f"Order created for user {dto.user_id} with amount {dto.amount}")
        return OrderCreated(order_id=order_id.id)
```

---

# 3️⃣ Infrastructure layer

```python
# core/infrastructure/db/models/order_models.py
from django.db import models

class OrderModel(models.Model):
    user_id = models.IntegerField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
```

```python
# core/infrastructure/db/repositories/order_repository.py
from core.application.interfaces.repositories import OrderRepository
from core.domain.order.entities import Order
from core.infrastructure.db.models.order_models import OrderModel

class DjangoOrderRepository(OrderRepository):
    def save(self, order: Order):
        obj = OrderModel.objects.create(
            user_id=order.user_id,
            amount=order.price.amount
        )
        # domain order_id bilan yangilanishi mumkin
        order.order_id.id = obj.id
```

```python
# core/infrastructure/services/external_service.py
class PaymentService:
    def charge(self, user_id: int, amount: float) -> bool:
        # Fake payment processing
        print(f"Charging user {user_id} amount {amount}")
        return True
```

---

# 4️⃣ Cross-cutting layer

```python
# cross_cutting/logging/logger.py
import logging

logger = logging.getLogger("app_logger")
logging.basicConfig(level=logging.INFO)
```

```python
# cross_cutting/validation/validator.py
def validate_positive(value: float, name: str):
    if value <= 0:
        raise ValueError(f"{name} must be positive")
```

---

# 5️⃣ API layer (DRF)

```python
# api/v1/serializers/order_serializers.py
from rest_framework import serializers

class CreateOrderSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    amount = serializers.FloatField()
```

```python
# api/v1/views/order_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from core.application.order.use_cases import CreateOrderUseCase
from core.application.order.dtos import CreateOrderDTO
from core.infrastructure.db.repositories.order_repository import DjangoOrderRepository
from cross_cutting.logging.logger import logger
from cross_cutting.validation.validator import validate_positive

from api.v1.serializers.order_serializers import CreateOrderSerializer

class CreateOrderView(APIView):
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data["user_id"]
        amount = serializer.validated_data["amount"]

        # cross-cutting validation
        validate_positive(amount, "amount")

        dto = CreateOrderDTO(user_id=user_id, amount=amount)
        use_case = CreateOrderUseCase(DjangoOrderRepository(), logger)
        event = use_case.execute(dto)
        return Response({"order_id": event.order_id})
```

```python
# api/v1/urls.py
from django.urls import path
from api.v1.views.order_views import CreateOrderView

urlpatterns = [
    path("orders/", CreateOrderView.as_view(), name="create_order"),
]
```

---

# 6️⃣ Flow diagram

```text
[ POST /api/v1/orders/ ]  <-- DRF View
       ↓
[ CreateOrderUseCase ]    <-- Application layer
       ↓
[ DjangoOrderRepository ] <-- Infrastructure
       ↓
[ OrderModel ]           <-- DB (ORM)
       ↓
[ OrderCreated Event ]   <-- Domain + Cross-cutting
```

* **DRF view**: faqat request → serializer → use case
* **Use case**: domain entity yaratadi, repository orqali DB ga yozadi, logger orqali log qiladi
* **Repository**: domain → ORM implementatsiyasi
* **Domain**: pure business rules, validation
* **Cross-cutting**: logger + validation

---

💡 **Afzalliklar**:

* Har layer mustaqil: unit test yozish oson
* Domain layer framework-agnostic
* Application layer testable, DB va DRF’dan mustaqil
* Infrastructure layer’ni kelajakda microservice sifatida ajratish mumkin

---

Agar xohlasang, men **shu misolni Django admin va migrations bilan to‘liq ishlaydigan holatda** berib, sen `python manage.py runserver` qilganingda endpoint ishlashini ko‘rsataman.

Shuni qilaylikmi?
