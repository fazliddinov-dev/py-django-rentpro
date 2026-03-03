Great question 🔥
I’ll show you a **Clean Architecture–style custom authentication** example based on your structure.

We’ll implement:

> ✅ Login with email + password
> ✅ JWT generation
> ✅ Clean separation (API → Application → Domain → Infrastructure)

---

# 📁 Final Structure (Relevant Parts)

```text
api/
  v1/
    views/
      auth_view.py
    serializers/
      auth_serializer.py

core/
  user/
    domain/
      entities/
        user.py
      services/
        password_hasher.py
    application/
      dto/
        auth_dto.py
      interfaces/
        user_repository.py
        token_service.py
      use_cases/
        login_user.py
    infrastructure/
      db/
        models/
          user_model.py
        repositories/
          django_user_repository.py
      services/
        jwt_token_service.py

container/
  user_container.py
```

---

# 1️⃣ Domain Layer (Pure Business Logic)

## 📄 `domain/entities/user.py`

```python
class User:
    def __init__(self, id: int, email: str, password_hash: str):
        self.id = id
        self.email = email
        self.password_hash = password_hash

    def verify_password(self, raw_password: str, hasher):
        return hasher.verify(raw_password, self.password_hash)
```

Domain does NOT know:

* Django
* JWT
* ORM

---

## 📄 `domain/services/password_hasher.py`

```python
from abc import ABC, abstractmethod

class PasswordHasher(ABC):
    @abstractmethod
    def verify(self, raw_password: str, hashed_password: str) -> bool:
        pass
```

Domain only defines contract.

---

# 2️⃣ Application Layer

## 📄 `application/interfaces/user_repository.py`

```python
from abc import ABC, abstractmethod
from core.user.domain.entities.user import User

class UserRepository(ABC):

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        pass
```

---

## 📄 `application/interfaces/token_service.py`

```python
from abc import ABC, abstractmethod

class TokenService(ABC):

    @abstractmethod
    def generate_access_token(self, user_id: int) -> str:
        pass
```

---

## 📄 `application/dto/auth_dto.py`

```python
class LoginInputDTO:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password


class LoginOutputDTO:
    def __init__(self, access_token: str):
        self.access_token = access_token
```

---

## 📄 `application/use_cases/login_user.py`

```python
class LoginUserUseCase:

    def __init__(self, user_repo, token_service, password_hasher):
        self.user_repo = user_repo
        self.token_service = token_service
        self.password_hasher = password_hasher

    def execute(self, input_dto):
        user = self.user_repo.get_by_email(input_dto.email)

        if not user:
            raise Exception("Invalid credentials")

        if not user.verify_password(input_dto.password, self.password_hasher):
            raise Exception("Invalid credentials")

        token = self.token_service.generate_access_token(user.id)

        return token
```

⚡ Notice:

* No Django
* No ORM
* No JWT
* No HTTP

Pure use case.

---

# 3️⃣ Infrastructure Layer

Assume we use:

* **Django**
* **PyJWT**

---

## 📄 `infrastructure/db/models/user_model.py`

```python
from django.db import models

class UserModel(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
```

---

## 📄 `infrastructure/db/repositories/django_user_repository.py`

```python
from core.user.domain.entities.user import User
from core.user.application.interfaces.user_repository import UserRepository
from .models.user_model import UserModel


class DjangoUserRepository(UserRepository):

    def get_by_email(self, email: str):
        try:
            obj = UserModel.objects.get(email=email)
            return User(
                id=obj.id,
                email=obj.email,
                password_hash=obj.password
            )
        except UserModel.DoesNotExist:
            return None
```

---

## 📄 `infrastructure/services/jwt_token_service.py`

```python
import jwt
from django.conf import settings
from core.user.application.interfaces.token_service import TokenService


class JWTTokenService(TokenService):

    def generate_access_token(self, user_id: int) -> str:
        payload = {"user_id": user_id}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
```

---

## 📄 `infrastructure/services/django_password_hasher.py`

```python
from django.contrib.auth.hashers import check_password
from core.user.domain.services.password_hasher import PasswordHasher


class DjangoPasswordHasher(PasswordHasher):

    def verify(self, raw_password: str, hashed_password: str) -> bool:
        return check_password(raw_password, hashed_password)
```

---

# 4️⃣ Container (Dependency Injection)

## 📄 `container/user_container.py`

```python
from core.user.application.use_cases.login_user import LoginUserUseCase
from core.user.infrastructure.db.repositories.django_user_repository import DjangoUserRepository
from core.user.infrastructure.services.jwt_token_service import JWTTokenService
from core.user.infrastructure.services.django_password_hasher import DjangoPasswordHasher


def login_user_use_case():
    return LoginUserUseCase(
        user_repo=DjangoUserRepository(),
        token_service=JWTTokenService(),
        password_hasher=DjangoPasswordHasher()
    )
```

Now everything is wired properly.

---

# 5️⃣ API Layer

## 📄 `api/v1/serializers/auth_serializer.py`

```python
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
```

---

## 📄 `api/v1/views/auth_view.py`

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from container.user_container import login_user_use_case
from core.user.application.dto.auth_dto import LoginInputDTO
from .serializers.auth_serializer import LoginSerializer


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto = LoginInputDTO(**serializer.validated_data)

        use_case = login_user_use_case()
        token = use_case.execute(dto)

        return Response({"access_token": token})
```

---

# 🔄 Flow

```text
HTTP Request
   ↓
APIView
   ↓
UseCase
   ↓
Repository
   ↓
Database
   ↓
Token Service
   ↓
Response
```

Clean. Replaceable. Testable.

---

# 🧠 Why This Is Powerful

You can now:

* Replace Django with FastAPI → no core change
* Replace JWT → only token service changes
* Replace DB → only repository changes
* Unit test LoginUserUseCase without Django

---

If you want next, I can show:

* Custom authentication middleware that validates JWT
* Refresh token implementation
* Role-based authorization (RBAC)
* Or convert this to FastAPI version 🚀
