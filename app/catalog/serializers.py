from rest_framework import serializers

from catalog.models import Category


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


class ProductSerializer(serializers.ModelSerializer):
	pass
