from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from baskets.models import Basket
from catalog.models import Product


def validator_product_id(value):
	product = Product.objects.filter(id=int(value))
	if not product.exists():
		raise ValidationError("не верный id продукта")


class BasketSerializer(serializers.Serializer):
	id = serializers.CharField(validators=[validator_product_id])
	quantity = serializers.IntegerField(min_value=1)


class ListBasketSerializer(serializers.ModelSerializer):
	id = serializers.CharField(source="product.id")
	category = serializers.SerializerMethodField()
	quantity = serializers.IntegerField()
	price = serializers.SerializerMethodField()
	title = serializers.SerializerMethodField()
	description = serializers.SerializerMethodField()
	href = serializers.SerializerMethodField()
	freeDelivery = serializers.SerializerMethodField()
	images = serializers.SerializerMethodField()
	tags = serializers.SerializerMethodField()
	reviews = serializers.SerializerMethodField()
	rating = serializers.SerializerMethodField()

	class Meta:
		model = Basket
		fields = [
			"id", "category", "price", "quantity",
			"date_created", "title", "description",
			"href", "freeDelivery", "images",
			"tags", "reviews", "rating",
		]

	@staticmethod
	def get_category(obj):
		print(obj)
		return str(obj.product.category)

	@staticmethod
	def get_title(obj):
		return obj.product.title

	@staticmethod
	def get_description(obj):
		return obj.product.full_description[:48] + '...'

	@staticmethod
	def get_href(obj):
		return f"/product/{obj.product.id}"

	@staticmethod
	def get_freeDelivery(obj):
		return obj.product.free_delivery

	@staticmethod
	def get_images(obj):
		return [image.src.url for image in obj.product.images.all()]

	@staticmethod
	def get_tags(obj):
		return [tag.title for tag in obj.product.tags.all()]

	@staticmethod
	def get_reviews(obj):
		return len(obj.product.reviews.all())

	@staticmethod
	def get_rating(obj):
		return obj.product.get_rating()

	@staticmethod
	def get_price(obj):
		return obj.product_price()
