import factory
from factory.django import DjangoModelFactory

from danube.accounts.models import User
from danube.chat.models import ChatRoom, Message
from danube.constants import DISCOUNT_TYPE_CHOICES
from danube.contracts.models import Contract, WorkItem
from danube.invoices.models import Invoice
from danube.profiles.models import TITLES_CHOICE, Property, BusinessDetails
from danube.quotes.models import RFQ, RFQItem, RFQBusinessRequest, EOI


class UserFactory(DjangoModelFactory):
    """User factory."""

    class Meta:
        """Meta."""

        model = User

    email = factory.Faker("email")
    username = factory.Faker("user_name")
    user_type = factory.Iterator(list(dict(User.ROLES_CHOICES).keys()))
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    date_joined = factory.Faker("past_datetime", start_date="-30d")
    is_superuser = False
    is_active = True


class PropertyFactory(DjangoModelFactory):
    class Meta:
        model = Property

    address_1 = factory.Faker("address")
    address_2 = factory.Faker("address")
    town = factory.Faker("city")
    city = factory.Faker("city")
    county = factory.Faker("country")
    postcode = factory.Faker("postcode")
    user = factory.SubFactory(UserFactory)


class BusinessDetailsFactory(DjangoModelFactory):
    class Meta:
        model = BusinessDetails

    user = factory.SubFactory(UserFactory)
    business_name = factory.Faker("first_name")
    website = factory.Faker("url")
    vat = factory.Faker("random_int", max=1000000000000)
    main_trade = factory.Faker("address")
    description = factory.Faker("text")
    company_number = factory.Faker("random_int", max=100000000, min=10000000)
    address_1 = factory.Faker("address")
    address_2 = factory.Faker("address")
    town = factory.Faker("city")
    city = factory.Faker("city")
    county = factory.Faker("country")
    postcode = factory.Faker("postcode")


class RFQFactory(DjangoModelFactory):
    class Meta:
        model = RFQ

    property = factory.SubFactory(PropertyFactory)
    title = factory.Faker("first_name")
    # status = factory.Iterator(list(dict(RFQ.STATUS_CHOICES).keys()))

class RFQItemFactory(DjangoModelFactory):
    class Meta:
        model = RFQItem

    rfq = factory.SubFactory(RFQFactory)
    area_of_work = factory.Faker("first_name")
    brief_description = factory.Faker("first_name")
    detailed_description = factory.Faker("text")
    comments = factory.Faker("text")


class RFQBusinessRequestFactory(DjangoModelFactory):
    class Meta:
        model = RFQBusinessRequest

    rfq = factory.SubFactory(RFQFactory)
    business_profile = factory.SubFactory(BusinessDetailsFactory)


class EOIFactory(DjangoModelFactory):
    class Meta:
        model = EOI

    business = factory.SubFactory(BusinessDetailsFactory)
    rfq = factory.SubFactory(RFQFactory)
    start_price = factory.Faker("random_int")
    comment = factory.Faker("text")


class ContractFactory(DjangoModelFactory):
    class Meta:
        model = Contract

    title = factory.Faker("first_name")
    status = factory.Iterator(list(dict(Contract.STATUS_CHOICES).keys()))
    property_obj = factory.SubFactory(PropertyFactory)
    business = factory.SubFactory(BusinessDetailsFactory)
    description = factory.Faker("text")
    eoi = factory.SubFactory(EOIFactory)
    vat = 0.00
    discount_type = factory.Iterator(list(dict(DISCOUNT_TYPE_CHOICES).keys()))
    discount = 0.00
    first_payment_amount = 0.00


class InvoiceFactory(DjangoModelFactory):
    class Meta:
        model = Invoice

    status = factory.Iterator(list(dict(Invoice.STATUS_CHOICES).keys()))
    property_obj = factory.SubFactory(PropertyFactory)
    business = factory.SubFactory(BusinessDetailsFactory)
    eoi = factory.SubFactory(EOIFactory)
    contract = factory.SubFactory(ContractFactory)


class WorkItemFactory(DjangoModelFactory):
    class Meta:
        model = WorkItem

    title = factory.Faker("first_name")
    contract = factory.SubFactory(ContractFactory)
    price = factory.Faker("random_int")
    description = factory.Faker("text")



class ChatRoomFactory(DjangoModelFactory):
    class Meta:
        model = ChatRoom

    author = factory.SubFactory(UserFactory)
    participant = factory.SubFactory(UserFactory)
    eoi = factory.SubFactory(EOIFactory)


class MessageFactory(DjangoModelFactory):
    class Meta:
        model = Message

    content = factory.Faker("text")
    author = factory.SubFactory(UserFactory)
    chat_room = factory.SubFactory(ChatRoomFactory)
