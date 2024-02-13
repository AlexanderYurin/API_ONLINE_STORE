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
		return Basket.objects.filter(session_key=self.request.session.session_key)

	@action(detail=False, methods="POST")
	def post_basket(self, request, *args, **kwargs):
		serializer = BasketSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		product_id = serializer.data.get("id")
		quantity = serializer.data.get("quantity")
		if request.user.is_authenticated:
			basket_user = Basket.objects.filter(user=request.user)
			products = basket_user.filter(product_id=product_id)
			if products.exists():
				basket = products.first()
				basket.quantity += quantity
				basket.save()
			else:
				Basket.objects.create(user=request.user, product_id=product_id, quantity=quantity)
		# else:
		# 	session_key = get_session_key(self.request)
		# 	baskets = Basket.objects.filter(session_key=session_key, product=product)
		# 	if baskets.exists():
		# 		basket = baskets.first()
		# 		basket.quantity += quantity
		# 		basket.save()
		# 	else:
		# 		Basket.objects.create(session_key=request.session.session_key, product=product, quantity=quantity)
		serializer = self.get_serializer(self.get_queryset(), many=True)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

		# if request.user.is_authenticated:
		# 	serializer.data["user"] = request.user
		# 	baskets = Basket.objects.filter(user=request.user, product=product)
		# else:
		# 	session_key = get_session_key(self.request)
		# 	serializer.data["session_key"] = session_key
		# 	baskets = Basket.objects.filter(session_key=session_key, product=product)
		#
		# if baskets.exists():
		# 	instance = baskets.first()
		# 	serializer =
		# 	serializer = BasketSerializer(data=request.data)
		# 	serializer.is_valid(raise_exception=True)
		# 	serializer.save(request=request, product_id=id)
		# print(serializer.data)
		# serializer.save(request=request, product_id=id)
		# serializer = BasketSerializer(data=request.data)

