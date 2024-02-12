from django.urls import path

from catalog.views import CategoryViewSet, CatalogViewSet, TagViewSet, ProductViewSet

urlpatterns = [
	path("categories/", CategoryViewSet.as_view({"get": "get_categories"})),
	path("catalog/", CatalogViewSet.as_view({"get": "get_catalog"})),
	path("catalog/<int:pk>/", CatalogViewSet.as_view({"get": "get_catalog_id"})),
	path("product/popular/", CatalogViewSet.as_view({"get": "get_catalog_popular"})),
	path("product/limit/", CatalogViewSet.as_view({"get": "get_catalog_limit"})),
	path("banners/", CatalogViewSet.as_view({"get": "get_banner"})),
	path("sales/", CatalogViewSet.as_view({"get": "get_sales"})),
	path("tags/", TagViewSet.as_view({"get": "list"})),
	path("products/<int:pk>", ProductViewSet.as_view({"get": "get_product_id"})),
	path("product<int:pk>/review", ProductViewSet.as_view({"post": "post_product_id_review"})),
]
