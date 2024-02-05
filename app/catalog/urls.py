from django.urls import path

from catalog.views import CategoryViewSet, CatalogViewSet

urlpatterns = [
	path('categories/', CategoryViewSet.as_view({"get": "get_categories"})),
	path('catalog/', CatalogViewSet.as_view({"get": "get_catalog"})),
	path('catalog/<int:pk>', CatalogViewSet.as_view({"get": "get_catalog_id"})),

]
