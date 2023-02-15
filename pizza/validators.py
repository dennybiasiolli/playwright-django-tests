from django.core.exceptions import ValidationError


def validate_ingredients(value: str):
    check_value = value.lower()
    if "pineapple" in check_value or "ananas" in check_value:
        raise ValidationError(f'"{value}" is not a valid ingredient')


def validate_pizza_name(value: str):
    check_value = value.lower()
    if "hawai" in check_value:
        raise ValidationError(
            f'"{value}" is not a pizza, it\'s a crime against humanity'
        )
