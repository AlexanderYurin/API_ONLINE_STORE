from django.db.models import Avg
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from catalog.models import Category, Product, TagProduct, Review
from catalog.pagination import CustomPagination
from catalog.serializers import CategorySerializer, ProductCatalogSerializer, ProductSaleSerializer, TagSerializer, \
	DetailCatalogSerializer, ReviewSerializer


class CategoryViewSet(GenericViewSet):
	"""
	Представление для получения списка категорий
	"""
	queryset = Category.objects.filter(parent=None)

	@action(detail=False, methods=["get"])
	def get_categories(self, request: Request) -> Response:
		serializer = CategorySerializer(self.queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class CatalogViewSet(ReadOnlyModelViewSet):
	"""
	Представление для получения списка товаров
	"""
	queryset = Product.objects.all()
	pagination_class = CustomPagination
	serializer_class = ProductCatalogSerializer

	def get_queryset(self):
		if self.action == "get_catalog_id":
			return self.queryset.filter(category__pk=self.kwargs[self.lookup_field]).order_by("-date")
		if self.action == "get_catalog_popular":
			return self.queryset.filter(reviews__isnull=False).annotate(
				total_rate=Avg("reviews__rate")).order_by("-total_rate")
		if self.action == "get_catalog_limit":
			return self.queryset.filter(quantity__range=(1, 20)).order_by("quantity")
		if self.action == "get_banner":
			return self.queryset.filter.order_by("-count")[:5]
		if self.action == "get_sales":
			self.serializer_class = ProductSaleSerializer
			return self.queryset.filter(discount__isnull=False).order_by("-discount__discount")
		return self.queryset

	def get_catalog(self, request):
		return super().list(request)

	def get_catalog_id(self, request, pk=None):
		return super().list(request)

	def get_catalog_popular(self, request):
		return super().list(request)

	def get_catalog_limit(self, request):
		return super().list(request)

	def get_banner(self, request):
		return super().list(request)

	def get_sales(self, request):
		return super().list(request)


class TagViewSet(ReadOnlyModelViewSet):
	"""
    Представление для получения всех тегов.
    """
	queryset = TagProduct.objects.all()
	serializer_class = TagSerializer


class ProductViewSet(ReadOnlyModelViewSet):
	queryset = Product.objects.all()
	serializer_class = DetailCatalogSerializer

	def get_product_id(self, request):
		return super().retrieve(request)


class ReviewCreate(CreateModelMixin, GenericViewSet):
	serializer_class = ReviewSerializer

	def post_product_id_review(self, request):
		return super().create(request)
