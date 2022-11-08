from django.core.validators import MinValueValidator, MaxValueValidator

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

PERCENT = 1
AMOUNT = 2
DISCOUNT_TYPE_CHOICES = (
        (PERCENT, "PERCENT"),
        (AMOUNT, "AMOUNT")
)