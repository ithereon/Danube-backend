from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from danube.contracts.models import Contract
from danube.invoices.models import Invoice
from danube.quotes.models import RFQItem, RFQ, RFQBusinessRequest, EOI


@receiver(post_save, sender=Contract)
def set_eoi_accepted(instance: Contract, **kwargs: dict) -> None:
    """Set EOI as accepted if Contract was created."""
    if instance.status == Contract.DRAFT:
        instance.eoi.status = EOI.ACCEPTED
        instance.eoi.save()
    """Set RFQ CONTRACTED if Contract was agreed."""
    if instance.status == Contract.IN_PROGRESS:
        instance.eoi.rfq.status = RFQ.CONTRACTED
        instance.eoi.rfq.save()


@receiver(post_save, sender=Contract)
def create_invoice(instance: Contract, **kwargs: dict) -> None:
    """create invoice if contract was accepted."""
    if instance.status == Contract.IN_PROGRESS and instance.first_payment_amount > 0:
        invoice = Invoice.objects.filter(contract=instance)
        if not invoice:
            Invoice.objects.create(
                contract=instance,
                business=instance.business,
                property_obj=instance.property_obj,
                eoi=instance.eoi
            )


@receiver(post_save, sender=Contract)
def create_final_invoice(instance: Contract, **kwargs: dict) -> None:
    """create invoice if contract was completed by business."""
    if instance.business_completed:
        invoice = Invoice.objects.filter(contract=instance)
        if not invoice:
            Invoice.objects.create(
                contract=instance,
                business=instance.business,
                property_obj=instance.property_obj,
                eoi=instance.eoi
            )
        else:
            invoice.update(status=Invoice.OPEN, status_business=Invoice.OPEN)
            # invoice.status = Invoice.OPEN
            # invoice.status_business = Invoice.OPEN
            # invoice.save()
