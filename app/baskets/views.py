from django.shortcuts import render
from rest_framework.mixins import ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from baskets.models import Basket
from baskets.serializers import BasketSerializer

from catalog.serializers import ProductCatalogSerializer
from users.utils import get_session_key


# Create your views here.
class BasketViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
	"""
	Представление для получения списка товаров
	"""
	serializer_class = BasketSerializer

	def get_queryset(self):
		if self.request.user.is_authenticated:
			return Basket.objects.filter(user=self.request.user)
		session_key = get_session_key(self.request)









