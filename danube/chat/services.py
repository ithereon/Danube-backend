from typing import Optional
from typing import Union

from common.exceptions import IntegrityException, ValidationException
from common.exceptions import ObjectNotFoundException
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import DateField
from django.db.models import OuterRef
from django.db.models import Subquery
from django.db.models.functions import Coalesce

from .models import ChatRoom
from .models import Message

User = get_user_model()


class MessageService:
    model = Message

    @classmethod
    def create(cls, content: Union[str, None], author: User, chat_room_id: str):
        try:
            msg = cls.model.objects.create(
                author=author, content=content, chat_room_id=chat_room_id
            )
            chat_room = ChatRoom.objects.get(id=chat_room_id)
            if author == chat_room.author:
                chat_room.new_from_author = True
            elif author == chat_room.participant:
                chat_room.new_from_participant = True
            else:
                raise ValidationException
            chat_room.save()
            return msg

        except IntegrityError as e:
            raise IntegrityException(str(e))
        except ValidationException as e:
            raise ValidationException(str(e))

    @classmethod
    def get_user_messages_by_chat_id(cls, chat_room_id: str):
        return Message.objects.filter(chat_room_id=chat_room_id).distinct()

    @classmethod
    def get_previous_message(cls, message: Message) -> Optional[Message]:
        return (
            Message.objects.filter(
                author_id=message.author_id, chat_room_id=message.chat_room_id
            )
            .exclude(id=message.pk)
            .order_by("-created_at")
            .first()
        )


class ChatRoomService:
    model = ChatRoom

    @classmethod
    def get(cls, **filters):
        chat_room = cls.model.objects.filter(**filters).order_by("-created_at").first()
        if not chat_room:
            raise ObjectNotFoundException("Chat with provided filters not found")
        return chat_room

    @classmethod
    def create(cls, author, participant, eoi=None):
        try:
            return cls.model.objects.create(
                author=author, participant=participant, eoi=eoi
            )
        except IntegrityError:
            raise IntegrityException("Can not create chat room")

    @classmethod
    def has_already_created(cls, author: User, participant: User):
        return cls.model.objects.filter(author=author, participant=participant).exists()

    @classmethod
    def filter(cls, **filters):
        return cls.model.objects.filter(**filters)

    @classmethod
    def get_user_chat_rooms(cls, user: User):
        qs = cls.model.objects.all()
        qs = qs.filter(participant=user) if user.is_employee else qs.filter(author=user)
        return qs.distinct()

    @classmethod
    def get_user_eoi_chat_rooms(cls, user: User):
        qs = cls.model.objects.all()
        qs = qs.filter(participant=user) if user.is_employee else qs.filter(author=user)
        return qs.distinct()

    @classmethod
    def get_user_eoi_chat_rooms_with_sub_queries(cls, user: User):
        latest_message = (
            Message.objects.filter(chat_room=OuterRef("id"))
            .order_by("-created_at")
            .values("created_at")[:1]
        )
        qs = cls.model.objects.all()
        qs = qs.filter(participant=user) if user.is_employee else qs.filter(author=user)
        qs = qs.annotate(
            _latest_message=Subquery(latest_message),
            latest_message=Coalesce(
                "_latest_message", "created_at", output_field=DateField()
            ),
        )
        return qs.distinct()
