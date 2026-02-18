$folders = @(
    "core\domain\user",
    "core\domain\order",
    "core\application\user",
    "core\application\order",
    "core\application\interfaces",
    "core\infrastructure\db\models",
    "core\infrastructure\db\repositories",
    "core\infrastructure\services",
    "api\v1\serializers",
    "api\v1\views"
)
foreach ($f in $folders) { mkdir $f -Force }

$files = @(
    "core\domain\user\entities.py",
    "core\domain\user\value_objects.py",
    "core\domain\user\aggregates.py",
    "core\domain\user\events.py",
    "core\domain\order\entities.py",
    "core\domain\order\value_objects.py",
    "core\domain\order\aggregates.py",
    "core\domain\order\events.py",
    "core\application\interfaces\repositories.py",
    "core\application\interfaces\services.py",
    "core\application\user\dtos.py",
    "core\application\user\use_cases.py",
    "core\application\user\services.py",
    "core\application\order\dtos.py",
    "core\application\order\use_cases.py",
    "core\application\order\services.py",
    "core\infrastructure\db\models\user_models.py",
    "core\infrastructure\db\models\order_models.py",
    "core\infrastructure\db\repositories\user_repository.py",
    "core\infrastructure\db\repositories\order_repository.py",
    "core\infrastructure\services\external_service.py",
    "api\v1\serializers\user_serializers.py",
    "api\v1\serializers\order_serializers.py",
    "api\v1\views\user_views.py",
    "api\v1\views\order_views.py",
    "api\v1\urls.py",
    "api\v1\schemas.py"
)
foreach ($fi in $files) { New-Item -ItemType File $fi -Force }
