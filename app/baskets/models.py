from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from catalog.models import Product
from users.models import User


class CartQuerySet(models.QuerySet):
	def total_price(self) -> int:
		return sum(cart.product_price() for cart in self)

	def total_quantity(self) -> int:
		if self:
			return sum(cart.quantity for cart in self)
		return 0


class Basket(models.Model):
	user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Пользователь",
							 related_name="basket", blank=True, null=True)
	product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name="Товар",
								related_name="basket", blank=True, null=True)
	quantity = models.PositiveIntegerField(default=1, verbose_name="Кол-во")
	session_key = models.CharField(max_length=32, blank=True, null=True)
	date_created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
	archived = models.BooleanField(default=False, verbose_name="В архиве")

	class Meta:
		db_table = "cart"
		verbose_name = "Корзина"
		verbose_name_plural = "Корзина"

	objects = CartQuerySet().as_manager()

	def product_price(self) -> float:
		return round(self.product.sell_price() * self.quantity, 2)

	def __str__(self):
		return f"Корзина: {self.user} | Товар: {self.product.title} | Количество: {self.quantity}"

# Create your models here.

# class Basket(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='basket')
#     count = models.IntegerField()
#     date = models.DateTimeField(auto_now_add=True)
#     archived = models.BooleanField(default=False)
#
#     class Meta:
#         verbose_name = 'Basket'
#         verbose_name_plural = 'Basket'
#
#     def price(self) -> int:
#         return self.product.price * self.count
#
#
# class Order(models.Model):
#     createdAt = models.DateTimeField(auto_created=True, auto_now_add=True)
#     fullName = models.CharField(max_length=255, blank=True)
#     email = models.EmailField(max_length=255, blank=True)
#     phone = models.CharField(max_length=12, blank=True)
#     city = models.CharField(max_length=128, blank=True)
#     address = models.CharField(max_length=255, blank=True)
#     deliveryType = models.CharField(max_length=128, blank=True)
#     paymentType = models.CharField(max_length=128, blank=True)
#     totalCost = models.PositiveIntegerField()
#     status = models.CharField(max_length=128, blank=True)
#     basket = models.ManyToManyField(Basket)
#
#
# class Payment(models.Model):
#     number = models.PositiveIntegerField(validators=[MinValueValidator(1000000000000000),
#                                                      MaxValueValidator(9999999999999999)])
#     name = models.CharField(max_length=255)
#     month = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
#     year = models.PositiveIntegerField(validators=[MinValueValidator(2023), MaxValueValidator(2030)])
#     code = models.PositiveIntegerField(validators=[MinValueValidator(100), MaxValueValidator(999)])

