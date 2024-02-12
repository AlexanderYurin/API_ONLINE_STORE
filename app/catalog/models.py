from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CharField
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
	title = models.CharField(max_length=128, verbose_name="Название")
	parent = TreeForeignKey(to="Category", on_delete=models.CASCADE, related_name="subcategories",
							null=True, blank=True, verbose_name="category")
	src = models.ImageField(upload_to="icons_category/", null=True, blank=True, verbose_name="Иконка")

	class MPTTMeta:
		order_insertion_by = ["title"]

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "Категорию"
		verbose_name_plural = "Категории"


class Product(models.Model):
	category = models.ForeignKey(to="Category", on_delete=models.CASCADE, related_name="products")
	price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name="Цена")
	quantity = models.PositiveIntegerField(verbose_name="Кол-во")
	date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
	title = models.CharField(max_length=128, verbose_name="Название")
	full_description = models.TextField(verbose_name="Описание")
	free_delivery = models.BooleanField(default=False, verbose_name="Бесплатная доставка")
	discount = models.ForeignKey(to="Discount", on_delete=models.CASCADE, related_name="products", blank=True,
								 null=True, default=0)

	class Meta:
		verbose_name = "Товар"
		verbose_name_plural = "Товары"
		ordering = ["price"]

	def __str__(self):
		return self.title

	def get_rating(self):
		instance = self.reviews.all()
		if len(instance) == 0:
			return 0
		rates_list = [review.rate for review in instance]
		rating = round(sum(rates_list) / len(rates_list), 2)
		return float(rating)

	def sell_price(self):
		if self.discount:
			return round(self.price - self.discount.discount * self.price / 100, 2)
		return self.price


class Discount(models.Model):
	discount = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],
										   verbose_name="Скидка")
	date_from = models.DateTimeField(auto_now_add=True, auto_created=True, verbose_name="Начало акции")
	date_to = models.DateTimeField(verbose_name="Конец акции")

	class Meta:
		verbose_name = "Скидка"
		verbose_name_plural = "Скидки"
		ordering = ["discount"]

	def __str__(self):
		return f"{self.discount}%"


class ImageProduct(models.Model):
	src = models.ImageField(upload_to="product_images/", null=True, blank=True, verbose_name="Название")
	product = models.ForeignKey(to="Product", on_delete=models.CASCADE, related_name="images")

	class Meta:
		verbose_name = "Изображение"
		verbose_name_plural = "Изображения"


class TagProduct(models.Model):
	title = models.CharField(max_length=128, verbose_name="Название")
	products = models.ManyToManyField(Product, related_name="tags")

	class Meta:
		verbose_name = "Тэг"
		verbose_name_plural = "Тэг"

	def __str__(self):
		return self.title


class Review(models.Model):
	author = models.CharField(max_length=255, verbose_name="Автор")
	text = models.TextField(verbose_name="Текст")
	email = models.EmailField(verbose_name="Емайл")
	rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Рейтинг")
	date = models.DateTimeField(auto_now_add=True, auto_created=True, verbose_name="Дата создания")
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")

	class Meta:
		verbose_name = "Отзыв"
		verbose_name_plural = "Отзывы"

	def __str__(self):
		return self.text


class Specification(models.Model):
	title = models.CharField(max_length=255, verbose_name="Название")
	value = models.CharField(max_length=128, verbose_name="Значение")
	products = models.ManyToManyField(Product, related_name="specifications")

	class Meta:
		verbose_name = "Спецификацию"
		verbose_name_plural = "Спецификации"
