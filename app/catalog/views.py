from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response

from catalog.models import Category, Product
from catalog.serializers import CategorySerializer, ProductCatalogSerializer


class CategoryViewSet(viewsets.GenericViewSet):
	"""
	Представление для получения списка категорий
	"""
	queryset = Category.objects.all()

	@action(detail=False, methods=["get"])
	def get_categories(self, request: Request) -> Response:
		serializer = CategorySerializer(self.queryset, many=True)
		return Response(serializer.data)


class CatalogViewSet(viewsets.GenericViewSet):
	"""
	Представление для получения списка товаров
	"""

	queryset = Product.objects.all()

	@action(detail=False, methods=["get"])
	def get_catalog(self, request):
		paginator = PageNumberPagination()
		page_objects = paginator.paginate_queryset(self.queryset, request)
		serializer = ProductCatalogSerializer(page_objects, many=True)
		response_data = {
			"items": serializer.data,
			"currentPage": paginator.page.number,
			"lastPage": paginator.page.paginator.num_pages,

		}
		return Response(response_data)

	@action(detail=False, methods=["get"])
	def get_catalog_id(self, request, pk):
		queryset = Product.objects.filter(category__pk=pk).order_by("-date")
		paginator = PageNumberPagination()
		page_objects = paginator.paginate_queryset(queryset, request)
		serializer = ProductCatalogSerializer(page_objects, many=True)
		response_data = {
			"items": serializer.data,
			"currentPage": paginator.page.number,
			"lastPage": paginator.page.paginator.num_pages,

		}
		return Response(response_data)
