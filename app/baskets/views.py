from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from baskets.models import Basket
from baskets.serializers import ListBasketSerializer, BasketSerializer
from catalog.models import Product

from catalog.serializers import ProductCatalogSerializer
from users.utils import get_session_key


# Create your views here.
class BasketViewSet(ListModelMixin, GenericViewSet):
	"""
	Представление для получения списка товаров
	"""
	serializer_class = ListBasketSerializer

	def get_queryset(self):
		if self.request.user.is_authenticated:
			return Basket.objects.filter(user=self.request.user)
		print(self.request.session.session_key)
		return Basket.objects.filter(session_key=self.request.session.session_key)

	@action(detail=False, methods="POST")
	def post_basket(self, request, *args, **kwargs):
		valid_data = BasketSerializer(data=request.data)
		valid_data.is_valid(raise_exception=True)
		product_id = valid_data.data.get("id")
		quantity = valid_data.data.get("quantity")
		baskets = self.get_basket_user(request, product_id)
		if baskets.exists():
			product = baskets.first()
			serializer = ListBasketSerializer(data=valid_data.data, instance=product)
		else:
			serializer = ListBasketSerializer(data=valid_data.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(request=request, quantity=quantity, product_id=product_id)

		return Response(serializer.data, status=status.HTTP_201_CREATED)

	@action(detail=False, methods="DELETE")
	def delete_product_in_basket(self, request, *args, **kwargs):
		valid_data = BasketSerializer(data=request.data)
		valid_data.is_valid(raise_exception=True)
		product_id = valid_data.data.get("id")
		quantity = valid_data.data.get("quantity")
		baskets = self.get_basket_user(request, product_id)
		if not baskets.exists():
			return Response(status=status.HTTP_400_BAD_REQUEST)
		product = baskets.first()
		serializer = ListBasketSerializer(data=valid_data.data, instance=product)
		serializer.is_valid(raise_exception=True)
		serializer.save(request=request, quantity=quantity, product_id=product_id)
		return Response(serializer.data)

	@staticmethod
	def get_basket_user(request, product_id):
		if request.user.is_authenticated:
			return Basket.objects.filter(user=request.user, product_id=product_id)
		else:
			session_key = get_session_key(request)
			return Basket.objects.filter(session_key=session_key, product_id=product_id)
