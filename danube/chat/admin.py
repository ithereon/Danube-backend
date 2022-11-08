from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from .models import Message, ChatRoom
from danube.accounts.models import User
from ..quotes.models import EOI


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


class MessageEOIFilter(SimpleListFilter):
    title = "EOI"
    parameter_name = "eoi"

    def lookups(self, request, model_admin):
        return [
            (eoi.id, eoi.rfq.title)
            for eoi in EOI.objects.filter(chat_room__isnull=False)
        ]

    def queryset(self, request, queryset):
        if self.value() == "All":
            return queryset
        if self.value():
            return queryset.filter(chat_room__eoi__id=self.value())


class ReceiverFilter(SimpleListFilter):
    title = "Receiver"
    parameter_name = "receiver"

    def lookups(self, request, model_admin):
        return [(user.id, user.email) for user in User.objects.all().distinct()]

    def queryset(self, request, queryset):
        if self.value() == "All":
            return queryset
        if self.value():
            return queryset.filter(chat_room__participant__id=self.value()).exclude(
                author__id=self.value()
            )


class SenderFilter(SimpleListFilter):
    title = "Sender"
    parameter_name = "sender"

    def lookups(self, request, model_admin):
        return [
            (user.id, user.email)
            for user in User.objects.filter(chat_room_author__isnull=False).distinct()
        ]

    def queryset(self, request, queryset):
        if self.value() == "All":
            return queryset
        if self.value():
            return queryset.filter(author__id=self.value())


class ChatRoomFilter(SimpleListFilter):
    title = "Chat"
    parameter_name = "chat"

    def lookups(self, request, model_admin):
        return [
            (
                chat_room.id,
                f'{getattr(chat_room.author, "email", "")} '
                f'and {getattr(chat_room.participant, "email", "")}',
            )
            for chat_room in ChatRoom.objects.all()
        ]

    def queryset(self, request, queryset):
        if self.value() == "All":
            return queryset
        if self.value():
            return queryset.filter(chat_room__id=self.value())


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "content", "created_at")
    list_filter = (MessageEOIFilter, SenderFilter, ReceiverFilter, ChatRoomFilter)

    def get_queryset(self, request):
        qs = super(MessageAdmin, self).get_queryset(request)
        return qs.exclude(chat_room__isnull=True)

    def sender(self, obj):
        return self.get_name(obj.author)

    def receiver(self, obj):
        if obj.author != obj.chat_room.author:
            return self.get_name(obj.chat_room.author)
        else:
            return self.get_name(obj.chat_room.participant)

    def get_name(self, user: User):
        if user.first_name and user.last_name:
            return "{} {} ({})".format(user.first_name, user.last_name, user.email)
        else:
            return user.email


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ["author", "participant", "eoi"]
