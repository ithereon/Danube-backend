from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum

from danube.constants import PERCENTAGE_VALIDATOR, DISCOUNT_TYPE_CHOICES, PERCENT, AMOUNT
from danube.profiles.models import Property, BusinessDetails
from danube.quotes.models import EOI


class Contract(models.Model):
    DRAFT = 1
    WAITING = 2
    IN_PROGRESS = 3
    DONE = 4
    REJECTED = 5
    STATUS_CHOICES = (
        (DRAFT, "DRAFT"),
        (WAITING, "WAITING"),
        (IN_PROGRESS, "IN_PROGRESS"),
        (DONE, "DONE"),
        (REJECTED, "REJECTED"),
    )
    title = models.CharField(max_length=300)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=DRAFT)
    business_completed = models.BooleanField(default=False)
    property_obj = models.ForeignKey(
        to=Property,
        verbose_name="property",
        on_delete=models.CASCADE,
        related_name="contract",
    )
    business = models.ForeignKey(
        to=BusinessDetails, on_delete=models.CASCADE, related_name="contract"
    )
    description = models.TextField(null=True, blank=True, max_length=500)
    eoi = models.ForeignKey(to=EOI, on_delete=models.CASCADE, related_name="contract")
    created_at = models.DateTimeField(auto_now_add=True)

    first_payment_amount = models.DecimalField(decimal_places=2, max_digits=8, default=Decimal(0))
    first_payment_paid = models.BooleanField(default=False)
    first_payment_paid_business = models.BooleanField(default=False)
    vat = models.DecimalField(decimal_places=2, max_digits=8, default=Decimal(0), validators=PERCENTAGE_VALIDATOR)
    discount_type = models.PositiveIntegerField(choices=DISCOUNT_TYPE_CHOICES, default=PERCENT)
    discount = models.DecimalField(decimal_places=2, max_digits=8, default=Decimal(0))

    class Meta:
        unique_together = (
            "business",
            "eoi",
        )
        ordering = ('-created_at',)

    @property
    def total_cost(self):
        total = WorkItem.objects.filter(contract=self).aggregate(TOTAL=Sum('price')).get('TOTAL') or 0.0
        return total.quantize(Decimal("0.01"))

    @property
    def discount_amount(self):
        amount = 0.0
        if self.discount_type == PERCENT:
            amount = self.total_cost * self.discount / 100
        return amount.quantize(Decimal("0.01"))

    @property
    def subtotal_after_discount(self):
        subtotal = self.total_cost - self.discount_amount
        return subtotal.quantize(Decimal("0.01"))

    @property
    def vat_amount(self):
        amount = self.subtotal_after_discount * self.vat / 100
        return amount.quantize(Decimal("0.01"))

    @property
    def total(self):
        total = self.subtotal_after_discount + self.vat_amount
        return total.quantize(Decimal("0.01"))

    @property
    def total_after_first_payment(self):
        total = self.total
        if self.first_payment_amount > 0:
            total = self.total - self.first_payment_amount
        return total.quantize(Decimal("0.01"))

    def clean(self):
        if self.discount_type == PERCENT and self.discount > 100:
            raise ValidationError('discount type and discount amount are not matching')
        elif self.discount_type == AMOUNT and self.discount > self.total_cost:
            raise ValidationError('discount type and discount amount are not matching')
        elif self.first_payment_amount < 0 or self.first_payment_amount > self.subtotal_after_discount:
            raise ValidationError('first payment must be between 0 and total cost')

    def __str__(self):
        return str(self.title)


class WorkItem(models.Model):
    title = models.CharField(max_length=300)
    contract = models.ForeignKey(
        to=Contract, on_delete=models.CASCADE, related_name="work_items"
    )
    price = models.DecimalField(decimal_places=2, max_digits=8)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.title)
