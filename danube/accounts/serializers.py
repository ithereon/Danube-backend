from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import TokenError

from danube.accounts.models import *
from danube.profiles.serializers import PropertySerializer, BusinessDetailsSerializer


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        if obj == "" and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == "" and self.allow_blank:
            return ""

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail("invalid_choice", input=data)


class UserSerializer(serializers.ModelSerializer):
    title = ChoiceField(choices=TITLES_CHOICE, required=False)
    properties = serializers.SerializerMethodField(method_name="get_property")

    def get_property(self, obj):
        if obj.is_customer:
            return PropertySerializer(obj.property, many=True).data
        elif obj.is_employee:
            return BusinessDetailsSerializer(obj.business_details, many=True).data

    def to_representation(self, instance):
        self.fields["user_type"] = serializers.CharField(source="get_user_type_display")
        return super().to_representation(instance)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "user_type",
            "title",
            "mobile",
            "properties",
        )
        read_only_fields = (
            "id",
            "username",
            "email",
            "user_type",
            "properties",
        )


class UserShortSerializer(serializers.ModelSerializer):
    is_property_created = serializers.SerializerMethodField(read_only=True, method_name="get_is_property_created")

    def to_representation(self, instance):
        self.fields["user_type"] = serializers.CharField(source="get_user_type_display")
        return super().to_representation(instance)

    def get_is_property_created(self, obj):
        return obj.property.exists() or obj.business_details.exists()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "user_type",
            "is_property_created",
        )


class RegisterSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        self.fields["usertype"] = serializers.CharField(source="get_user_type_display")
        return super().to_representation(instance)

    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)
    usertype = ChoiceField(
        write_only=True, required=True, choices=User.REGISTRATION_ROLE_CHOICES
    )

    default_error_messages = {
        "email": "The username should only contain email characters"
    }

    class Meta:
        model = User
        fields = ("username", "password", "password2", "email", "usertype")

    def validate(self, attrs):
        username = attrs.get("username", "")

        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            user_type=validated_data["usertype"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ["token"]


class LoginSerializer(TokenObtainPairSerializer):
    def get_token(self, user: User) -> RefreshToken:
        """
        Get token for the user.
        """
        token: RefreshToken = RefreshToken.for_user(user)
        token["user"] = UserShortSerializer(user, context=self.context).data
        return token

    def validate(self, attrs: dict) -> dict:
        """
        Validate serializer.
        """
        super().validate(attrs)
        refresh: RefreshToken = self.get_token(self.user)
        data: dict = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserShortSerializer(self.user, context=self.context).data,
        }
        return data


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        filtered_user_by_email = User.objects.filter(email=email)
        print(filtered_user_by_email)
        user = auth.authenticate(email=email, password=password)

        if not filtered_user_by_email.exists():
            raise AuthenticationFailed(detail="Account doesn't exist")

        if not filtered_user_by_email[0].is_active:
            raise AuthenticationFailed("Account not activate, Kindly check your email")

        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")

        attrs["user"] = user
        attrs["id"] = user.id
        return attrs


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ["email"]


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)

            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise AuthenticationFailed("The reset link is invalid", 401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {"bad_token": ("Token is expired or invalid")}

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail("bad_token")
