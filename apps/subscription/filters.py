import django_filters
from rest_framework import filters

from .models import Plan


class SubscriptionProductFilter(django_filters.FilterSet):
    class Meta:
        model = Plan
        fields = {
            "name": ["exact", "icontains"],
            "regular_price": ["exact", "gte", "lte"],
            "sale_price": ["exact", "gte", "lte"],
            "sms_count": ["exact", "gte", "lte"],
            "stock_count": ["exact", "gte", "lte"],
            "length": ["exact", "gte", "lte"],
            "period": ["exact"],
        }
