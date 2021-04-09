from django.contrib.auth import get_user_model

from django.contrib.auth.password_validation import validate_password
from rest_framework import fields


from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.validators import UniqueValidator


class AuthSerializer(Serializer):
    """simple serializer to be used as a form for user auth"""
    password = fields.CharField(required=True)
    username = fields.CharField(required=True)


# @extend_schema_serializer(exclude_fields=('id', 'auth_token'))  # schema ignore these fields
class UserSerializer(ModelSerializer):
    password = fields.CharField(required=True, validators=[validate_password], write_only=True)
    username = fields.CharField(required=True, validators=[UniqueValidator(queryset=Meta.model.objects.all())])
    Authorization = fields.CharField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'type', 'first_name', 'last_name', 'email', 'password', 'Authorization')

        extra_kwargs = {
            'id': {'read_only': True},
            'type': {'read_only': True},
            # 'auth_token': {'read_only': True},
            'password': {'write_only': True},

        }

    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model

        validated_data.update({'username': validated_data['email']})
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

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        if 'email' in validated_data:
            instance.username = validated_data['email']

        instance.save()

        return instance