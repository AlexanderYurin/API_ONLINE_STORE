from django.urls import path

from baskets.views import BasketViewSet


urlpatterns = [
	path("", BasketViewSet.as_view({"get": "list", "post": "post_basket", "delete": "delete_product_in_basket"})),

]
