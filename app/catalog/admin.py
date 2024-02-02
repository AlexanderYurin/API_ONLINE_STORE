from django.contrib import admin

from catalog.models import Category, Product, ImageProduct, TagProduct, Review, Specification


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	pass


@admin.register(ImageProduct)
class ImageProductAdmin(admin.ModelAdmin):
	pass


@admin.register(TagProduct)
class TagProductAdmin(admin.ModelAdmin):
	pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	pass


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
	pass
