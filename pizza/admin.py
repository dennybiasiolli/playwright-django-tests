from django.contrib import admin
from django.db.models import Sum

from .models import Ingredient, Pizza


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ["name", "ingredients_list", "price"]

    def ingredients_list(self, obj):
        return ", ".join([i.name for i in obj.ingredients.all()])

    def price(self, obj):
        return obj.ingredients.all().aggregate(price=Sum("price"))["price"]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]
