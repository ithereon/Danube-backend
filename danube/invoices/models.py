from django.db import models

from danube.contracts.models import Contract
from danube.profiles.models import Property, BusinessDetails
from danube.quotes.models import EOI


class Invoice(models.Model):
    OPEN = 1
    PENDING = 2
    PAID = 3
    STATUS_CHOICES = (
        (OPEN, "OPEN"),
        (PENDING, "PENDING"),
        (PAID, "PAID"),
    )
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=OPEN)
    status_business = models.PositiveIntegerField(choices=STATUS_CHOICES, default=OPEN)
    property_obj = models.ForeignKey(
        to=Property,
        verbose_name="property",
        on_delete=models.CASCADE,
        related_name="invoice",
    )
    business = models.ForeignKey(
        to=BusinessDetails, on_delete=models.CASCADE, related_name="invoice"
    )
    eoi = models.ForeignKey(to=EOI, on_delete=models.CASCADE, related_name="invoice")
    contract = models.ForeignKey(to=Contract, on_delete=models.CASCADE, related_name="invoice")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.status)

