uv add django djangorestframework djangorestframework-simplejwt black isort mypy flake8 flake8-django python-dotenv psycopg[binary] django-cors-headers structlog pytest pytest-django factory-boy faker

3️⃣ Core layerlarni yaratish (Clean Architecture skeleti)
mkdir -p core/domain core/application core/infrastructure
touch core/{__init__.py}
touch core/domain/{__init__.py}
touch core/application/{__init__.py}
touch core/infrastructure/{__init__.py}


Keyin sen aytgan DDD tuzilmani qo‘sh:

mkdir -p core/domain/user core/domain/order
touch core/domain/user/{__init__.py,entities.py,value_objects.py,aggregates.py,events.py}
touch core/domain/order/{__init__.py,entities.py,value_objects.py,aggregates.py,events.py}

4️⃣ Application layer (use cases + interfaces)
mkdir -p core/application/interfaces
touch core/application/interfaces/{__init__.py,repositories.py,services.py}

mkdir -p core/application/user core/application/order
touch core/application/user/{__init__.py,dtos.py,use_cases.py,services.py}
touch core/application/order/{__init__.py,dtos.py,use_cases.py,services.py}

5️⃣ Infrastructure layer (Django ORM shu yerda yashaydi)
mkdir -p core/infrastructure/db/models core/infrastructure/db/repositories core/infrastructure/services
touch core/infrastructure/{__init__.py}
touch core/infrastructure/db/{__init__.py}
touch core/infrastructure/db/models/{__init__.py,user_models.py,order_models.py}
touch core/infrastructure/db/repositories/{__init__.py,user_repository.py,order_repository.py}
touch core/infrastructure/services/{__init__.py,external_service.py}

7️⃣ API layer (DRF delivery mechanism)
mkdir -p api/v1/{serializers,views}
touch api/{__init__.py}
touch api/v1/{__init__.py,urls.py,schemas.py}
touch api/v1/serializers/{__init__.py,user_serializers.py,order_serializers.py}
touch api/v1/views/{__init__.py,user_views.py,order_views.py}