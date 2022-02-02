from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import authenticate

from .models import User, Invite


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    msg = _("User account is disabled.")
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to log in with provided credentials."
                raise ValidationError(msg)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        data["user"] = user
        return data


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True}}

    # def validate(self, attrs):
    #     email = attrs['email']
    #     if self.Meta.model.objects.filter(email=email).exists():
    #         raise ValidationError('This email is already in use.')
    #     return attrs

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = ("email", "member_type", "space")
