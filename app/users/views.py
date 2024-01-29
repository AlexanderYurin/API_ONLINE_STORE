from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


# Create your views here.
class UserViewSet(viewsets.ViewSet):
	"""
	Набор представлений, предоставляющий стандартные действия
	пользователя
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer

	@action(detail=True, methods=["get"])
	def get_profile(self, request, pk=None):
		pass

	@action(detail=True, methods=["post"])
	def post_profile(self, request, pk=None):
		pass

	@action(detail=True, methods=["post"])
	def post_avatar(self, request, pk=None):
		pass

	@action(detail=True, methods=["post"])
	def post_password(self, request, pk=None):
		pass

def index():
	pass


def avatar():
	pass


def password():
	pass
