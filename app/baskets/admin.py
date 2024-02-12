from django.contrib import admin

from baskets.models import Basket


# Register your models here.

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
	pass

