# Generated by Django 4.1.7 on 2023-02-15 21:12

from django.db import migrations, models
import pizza.validators


class Migration(migrations.Migration):
    dependencies = [
        ("pizza", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="name",
            field=models.CharField(
                max_length=100, validators=[pizza.validators.validate_ingredients]
            ),
        ),
        migrations.AlterField(
            model_name="pizza",
            name="name",
            field=models.CharField(
                max_length=100,
                validators=[
                    pizza.validators.validate_ingredients,
                    pizza.validators.validate_pizza_name,
                ],
            ),
        ),
    ]
