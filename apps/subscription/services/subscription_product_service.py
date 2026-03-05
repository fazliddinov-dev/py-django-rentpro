from ..models import SubscriptionProducts


class SubscriptionProductService:
    @staticmethod
    def get_all_products():
        return SubscriptionProducts.objects.all()

    @staticmethod
    def get_product_by_id(product_id):
        try:
            return SubscriptionProducts.objects.get(id=product_id)
        except SubscriptionProducts.DoesNotExist:
            return None

    @staticmethod
    def create_product(validated_data):
        return SubscriptionProducts.objects.create(**validated_data)

    @staticmethod
    def update_product(product_id, validated_data):
        try:
            product = SubscriptionProducts.objects.get(id=product_id)
        except SubscriptionProducts.DoesNotExist:
            return None

        for attr, value in validated_data.items():
            setattr(product, attr, value)

        product.save()
        return product
