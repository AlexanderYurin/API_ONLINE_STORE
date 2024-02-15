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
	id = serializers.SerializerMethodField()
	category = serializers.SerializerMethodField()
	count = serializers.SerializerMethodField()
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
			"id", "category", "price", "count",
			"date_created", "title", "description",
			"href", "freeDelivery", "images",
			"tags", "reviews", "rating",
		]

	def create(self, validated_data):
		if validated_data.get("request").user:
			return Basket.objects.create(user=validated_data.get("request").user,
										 product_id=validated_data.get("product_id"),
										 quantity=validated_data.get("quantity"))
		return Basket.objects.create(session_key=validated_data.get("session_key"),
									 product_id=validated_data.get("product_id"),
									 quantity=validated_data.get("quantity"))

	def update(self, instance, validated_data):
		if validated_data["request"].method == "DELETE":
			instance.quantity -= validated_data.get("quantity")
			if instance.quantity < 1:
				return instance.delete()
		else:
			instance.quantity += validated_data.get("quantity")
		instance.save()
		return instance
	@staticmethod
	def get_id(obj):
		print(obj)
		return str(obj.product.id)

	@staticmethod
	def get_count(obj):
		return obj.quantity

	@staticmethod
	def get_category(obj):
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
