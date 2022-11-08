from django.contrib import admin

from danube.quotes.models import RFQ, RFQItem, RFQBusinessRequest, EOI

admin.site.register(RFQ)
admin.site.register(RFQItem)
admin.site.register(RFQBusinessRequest)
admin.site.register(EOI)
