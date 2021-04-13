"""
project DRF serializers for users and categories
"""
import traceback

from django.contrib.auth import get_user_model

from django.contrib.auth.password_validation import validate_password
from rest_framework import fields
from rest_framework.authtoken.models import Token

from rest_framework.serializers import Serializer, ModelSerializer, raise_errors_on_nested_writes
from rest_framework.validators import UniqueValidator

from .models import UpperCategory, InnerCategory


class InnerCategorySerializer(ModelSerializer):
    upper_category_id = fields.IntegerField(write_only=True)

    class Meta:
        model = InnerCategory
        fields = ('id', 'name', 'description', 'upper_category_id')

        extra_kwargs = {
            'id': {'read_only': True}
        }


class UpperCategorySerializer(ModelSerializer):
    inner_categories = InnerCategorySerializer(many=True, read_only=True)

    class Meta:
        model = UpperCategory
        fields = '__all__'

        extra_kwargs = {
            'id': {'read_only': True}
        }


class AuthSerializer(Serializer):
    """simple serializer to be used as a form for user auth"""
    password = fields.CharField(required=True)
    username = fields.CharField(required=True)


# @extend_schema_serializer(exclude_fields=('id', 'auth_token'))  # schema ignore these fields
class UserSerializer(ModelSerializer):
    password = fields.CharField(required=True, validators=[validate_password], write_only=True)
    username = fields.CharField(required=True, validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    Authorization = fields.CharField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password', 'Authorization')

        extra_kwargs = {
            'id': {'read_only': True},

            'password': {'write_only': True},

        }

    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model

        try:
            user = ModelClass._default_manager.create_user(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                    'Got a `TypeError` when calling `%s.%s.create()`. '
                    'This may be because you have a writable field on the '
                    'serializer class that is not a valid argument to '
                    '`%s.%s.create()`. You may need to make the field '
                    'read-only, or override the %s.create() method to handle '
                    'this correctly.\nOriginal exception was:\n %s' %
                    (
                        ModelClass.__name__,
                        ModelClass._default_manager.name,
                        ModelClass.__name__,
                        ModelClass._default_manager.name,
                        self.__class__.__name__,
                        tb
                    )
            )
            raise TypeError(msg)
        token = Token.objects.create(user_id=user.id)
        self.data.update({'Authorization': f'Token {token.key}'})
        self._data.update({'Authorization': f'Token {token.key}'})

        # self.validated_data.update({'Authorization': f'Token {token.key}'})
        # self.initial_data.update({'Authorization': f'Token {token.key}'})
        # self._validated_data.update({'Authorization': f'Token {token.key}'})
        return user

    def update(self, instance, validated_data):

        raise_errors_on_nested_writes('update', self, validated_data)
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance
