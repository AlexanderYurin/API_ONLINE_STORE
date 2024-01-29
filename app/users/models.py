from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


# Create your models here.
class User(AbstractUser):
	phone = models.CharField(validators=[RegexValidator(
		regex="\d{10}",
		message="Не верный формат номера"
	)])
	avatar = models.ImageField(upload_to="user_images", blank=True, null=True)

	class Meta:
		db_table = "user"
		verbose_name = "Пользователя"
		verbose_name_plural = "Пользователи"

	def __str__(self):
		return self.username
