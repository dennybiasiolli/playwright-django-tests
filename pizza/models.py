from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self) -> str:
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self) -> str:
        return self.name
