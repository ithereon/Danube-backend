from django.db import models

from danube.profiles.models import Property, BusinessDetails


class RFQ(models.Model):
    DRAFT = 1
    SAVED = 2
    OPEN = 3
    PRIVATE = 4
    CONTRACTED = 5
    ARCHIVED = 6
    COMPLETED = 7
    ACTIVE = 8

    STATUS_CHOICES = [
        (DRAFT, "DRAFT"),
        (SAVED, "SAVED"),
        (OPEN, "OPEN"),
        (PRIVATE, "PRIVATE"),
        (CONTRACTED, "CONTRACTED"),
        (ARCHIVED, "ARCHIVED"),
        (COMPLETED, "COMPLETED"),
    ]
    title = models.CharField(max_length=200)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=DRAFT)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="rfq",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.title)


class RFQItem(models.Model):
    rfq = models.ForeignKey(RFQ, on_delete=models.CASCADE, related_name="rfq_items")
    area_of_work = models.CharField(max_length=30)
    brief_description = models.CharField(max_length=200)

    detailed_description = models.TextField()
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.area_of_work)


class RFQBusinessRequest(models.Model):
    WAITING = 1
    CLOSED = 2
    ARCHIVED = 3
    DECLINED = 4
    STATUS_CHOICES = [
        (WAITING, "WAITING"),
        (CLOSED, "CLOSED"),
        (ARCHIVED, "ARCHIVED"),
        (DECLINED, "DECLINED"),
    ]
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=WAITING)
    rfq = models.ForeignKey(
        to=RFQ, related_name="business_request", on_delete=models.CASCADE
    )
    business_profile = models.ForeignKey(
        to=BusinessDetails, related_name="business_request", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["rfq", "business_profile"]
        ordering = ('-created_at',)


class EOI(models.Model):
    NEW = 1
    ACCEPTED = 2
    DECLINED = 3
    STATUS_CHOICES = [
        (NEW, "NEW"),
        (ACCEPTED, "ACCEPTED"),
        (DECLINED, "DECLINED"),
    ]
    business = models.ForeignKey(
        BusinessDetails, on_delete=models.CASCADE, related_name="eoi"
    )
    rfq = models.ForeignKey(RFQ, on_delete=models.CASCADE, related_name="eoi")
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=NEW)
    start_price = models.PositiveIntegerField(default=1)
    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["rfq", "business"]
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.pk)
