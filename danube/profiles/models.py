from django.core.validators import int_list_validator, MinLengthValidator
from django.db import models

from danube.accounts.models import User

MR = 1
MS = 2
MRS = 3
DR = 4
MISS = 5
THEM = 6
THEY = 7
HE = 8
SHE = 9

TITLES_CHOICE = (
    (MR, "Mr"),
    (MS, "Ms"),
    (MRS, "Mrs"),
    (DR, "Dr"),
    (MISS, "Miss"),
    (THEM, "Them"),
    (THEY, "They"),
    (HE, "He"),
    (SHE, "She"),
)


class AbstractDetails(models.Model):
    address_1 = models.CharField(max_length=300)
    address_2 = models.CharField(max_length=400, null=True, blank=True)
    town = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    county = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="details")

    class Meta:
        abstract = True


class Property(AbstractDetails):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="property")

    def __str__(self):
        return self.address_1

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Property"


class BusinessDetails(AbstractDetails):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="business_details"
    )
    business_name = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=200, blank=True)
    vat = models.CharField(
        max_length=12, default=None, blank=True, null=True, help_text="VAT number"
    )
    main_trade = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    company_number = models.CharField(
        max_length=8,
        validators=[int_list_validator(sep=""), MinLengthValidator(8), ],
        blank=True,
    )

    def __str__(self):
        return self.business_name

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Business Details"
