from django.db import models

from .validators import validate_ingredients, validate_pizza_name


class Ingredient(models.Model):
    name = models.CharField(max_length=100, validators=[validate_ingredients])
    price = models.FloatField()

    def __str__(self) -> str:
        return self.name


class Pizza(models.Model):
    name = models.CharField(
        max_length=100, validators=[validate_ingredients, validate_pizza_name]
    )
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self) -> str:
        return self.name
