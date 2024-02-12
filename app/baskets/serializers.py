from rest_framework import serializers

from baskets.models import Basket
from catalog.serializers import ProductCatalogSerializer


class BasketSerializer(serializers.ModelSerializer):
	product = ProductCatalogSerializer()

	class Meta:
		model = Basket
		fields = "__all__"

