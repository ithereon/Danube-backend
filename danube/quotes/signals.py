from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from danube.quotes.models import RFQItem, RFQ, RFQBusinessRequest, EOI


@receiver(post_save, sender=RFQItem)
def check_rfq_status(instance: RFQItem, **kwargs: dict) -> None:
    """Check that RFQ status corresponds RFQ Item state."""
    if instance.rfq.status == RFQ.DRAFT:
        instance.rfq.status = RFQ.SAVED
        instance.rfq.save()


@receiver(post_delete, sender=RFQItem)
def check_rfq_status_draft(instance: RFQItem, **kwargs: dict) -> None:
    """Return SAVED to DRAFT if all Items was removed."""
    rfq = instance.rfq
    if rfq.status == RFQ.SAVED and rfq.rfq_items.count() == 0:
        rfq.status = RFQ.DRAFT
        rfq.save()


@receiver(post_save, sender=RFQBusinessRequest)
def set_rfq_private(instance: RFQBusinessRequest, **kwargs: dict) -> None:
    """Set RFQ to PRIVATE if request for business was created."""
    rfq = instance.rfq
    if rfq.status in (RFQ.SAVED, RFQ.OPEN):
        rfq.status = RFQ.PRIVATE
        rfq.save()

    """Set business RFQ status to CLOSED and rfq status to ACTIVE if EOI was created."""
    eoi = EOI.objects.filter(rfq=instance.rfq, business=instance.business_profile).last()
    if eoi:
        rfq.status = RFQ.ACTIVE
        rfq.save()
        instance.status = RFQBusinessRequest.CLOSED
        instance.save()
