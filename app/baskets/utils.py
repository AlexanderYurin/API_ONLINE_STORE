from django.db.models.manager import BaseManager
from django.http import HttpRequest


from users.utils import get_session_key

from baskets.models import Basket


def get_user_cart(request) -> BaseManager:
	if request.user.is_authenticated:
		return Basket.objects.filter(user=request.user)
	return Basket.objects.filter(session_key=get_session_key(request))