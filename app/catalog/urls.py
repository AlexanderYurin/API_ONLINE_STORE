from django.urls import path
from rest_framework.routers import DefaultRouter

from catalog.views import CategoryViewSet

urlpatterns = [
	path('categories/', CategoryViewSet.as_view({"get": "get_categories"})),

]
