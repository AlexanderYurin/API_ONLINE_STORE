from rest_framework import serializers

from catalog.models import Category, Product, Review, Specification, TagProduct


class SubcategoriesSerializer(serializers.ModelSerializer):
	image = serializers.SerializerMethodField()
	href = serializers.SerializerMethodField()
	id = serializers.CharField()

	class Meta:
		model = Category
		fields = [
			"id",
			"title",
			"image",
			"href",
		]

	@staticmethod
	def get_href(obj):
		return f"/catalog/{obj.pk}"

	@staticmethod
	def get_image(obj):
		alt = obj.src.name[6:]
		src = obj.src.url
		return {"alt": alt, "src": src}


class CategorySerializer(SubcategoriesSerializer):
	subcategories = serializers.SerializerMethodField()

	class Meta:
		model = Category
		fields = [
			"id",
			"title",
			"image",
			"href",
			"subcategories"
		]

	@staticmethod
	def get_subcategories(obj) -> serializers:
		if obj.subcategories.exists():
			subcategories = [subcat for subcat in obj.subcategories.all()]
			return SubcategoriesSerializer(subcategories, many=True).data


class TagsSerializer(serializers.ModelSerializer):
	id = serializers.SerializerMethodField()
	name = serializers.SerializerMethodField()

	class Meta:
		model = TagProduct
		fields = ["id", "name"]

	@staticmethod
	def get_id(obj):
		return obj.title.lower()


class ReviewSerializer(serializers.ModelSerializer):
	date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

	class Meta:
		model = Review
		fields = ["author", "email", "text", "rate", "date"]

	# def create(self, validated_data: dict):
	#     return Review.objects.create(
	#         author=validated_data.get('author'),
	#         email=validated_data.get('email'),
	#         text=validated_data.get('text'),
	#         rate=validated_data.get('rate'),
	#         product_id=validated_data.get('product_id')
	#     )


class SpecificationSerializer(serializers.ModelSerializer):
	name = serializers.SerializerMethodField()

	class Meta:
		model = Specification
		fields = ["name", "value"]

	@staticmethod
	def get_id(obj):
		return obj.title


class ProductCatalogSerializer(serializers.ModelSerializer):
	id = serializers.CharField()
	count = serializers.SerializerMethodField()
	date = serializers.DateTimeField(format='%a %b %d %Y %H:%M:%S %Z%z')
	description = serializers.SerializerMethodField()
	href = serializers.SerializerMethodField()
	images = serializers.SerializerMethodField()
	tags = serializers.SerializerMethodField()
	reviews = serializers.SerializerMethodField()
	rating = serializers.SerializerMethodField()

	class Meta:
		model = Product
		fields = [
			"id", "category", "price",
			"count", "date", "title",
			"description", "href", "freeDelivery",
			"images", "tags", "reviews",
			"rating",
		]

	@staticmethod
	def get_count(obj):
		return obj.quantity

	@staticmethod
	def get_description(obj) -> str:
		return obj.description[:48] + '...'

	@staticmethod
	def get_href(obj):
		return f"/product/{obj.pk}"

	@staticmethod
	def get_images(obj):
		return [image.src.url for image in obj.images.all()]

	@staticmethod
	def get_tags(obj):
		return [tag.title for tag in obj.tags.all()]

	@staticmethod
	def get_reviews(obj):
		return len(obj.reviews.all())

	@staticmethod
	def get_rating(obj):
		return obj.get_rating()


class DetailCatalogSerializer(ProductCatalogSerializer):
	fullDescription = serializers.SerializerMethodField()
	specifications = serializers.SerializerMethodField()

	class Meta:
		model = Product
		fields = [
			"id", "category", "price",
			"count", "date", "title",
			"description", "fullDescription", "href",
			"freeDelivery", "images", "tags",
			"specifications", "reviews", "rating",
		]

	@staticmethod
	def get_fullDescription(obj):
		return obj.description

	@staticmethod
	def get_reviews(obj):
		if obj.reviews.exists():
			reviews = [review for review in obj.reviews.all()]
			return ReviewSerializer(reviews, many=True).data
		return []

	@staticmethod
	def get_specifications(obj):
		if obj.specifications.exists():
			specs = [spec for spec in obj.specifications.all()]
			return SpecificationSerializer(specs, many=True).data
		return []
