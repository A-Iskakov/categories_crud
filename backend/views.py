"""
project views for users and categories
"""
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet, ModelViewSet

from backend.models import UpperCategory, InnerCategory
from backend.serializers import UserSerializer, AuthSerializer, UpperCategorySerializer, InnerCategorySerializer
from utils.responses import ResponseCreated, ResponseBadRequest, ResponseOk, ResponseForbidden


class UpperCategoryViewset(ModelViewSet):
    """
    API directory for upper categories
    """
    queryset = UpperCategory.objects.all()
    serializer_class = UpperCategorySerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action not in {'list', 'retrieve'}:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

class InnerCategoryViewset(UpperCategoryViewset):
    """
    API directory for inner categories
    """
    queryset = InnerCategory.objects.all()
    serializer_class = InnerCategorySerializer

class UserAccountViewSet(ViewSet):
    """
    API directory for user accounts
    """

    serializer_class = UserSerializer

    # @extend_schema(parameters=[UserSerializer])
    @action(detail=False, methods=['post'], name='register')
    def register(self, request):
        """
        register user
        """

        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():

            user_serializer.save()
            return ResponseCreated(user_serializer.data)
        else:
            return ResponseBadRequest(user_serializer.errors)

    @extend_schema(request=AuthSerializer)
    @action(detail=False, methods=['post'], name='login')
    def login(self, request, *args, **kwargs):
        """
        auth user
        """

        auth_form = AuthSerializer(data=request.data)
        if auth_form.is_valid():
            user = authenticate(username=request.data['username'], password=request.data['password'])

            if user is not None and user.is_active:
                try:
                    token = user.auth_token
                except ObjectDoesNotExist:
                    token = Token.objects.create(user_id=user.id)

                return ResponseOk({'Authorization': f'Token {token.key}'})

            return ResponseForbidden('Не удалось авторизовать')

        return ResponseBadRequest('Не указаны все необходимые аргументы')

    @action(detail=False, methods=['get'], name='logout', permission_classes=[IsAuthenticated])
    def logout(self, request, *args, **kwargs):
        """
        logout session
        """

        Token.objects.filter(user_id=request.user.id).delete()
        return ResponseOk({'Logout': 'Success'})

    @action(detail=False, methods=['get'], name='my_profile_details',
            permission_classes=[IsAuthenticated]
            )
    def my_profile_details(self, request, *args, **kwargs):
        """
         get current user profile details
        """

        user_serializer = UserSerializer(request.user)
        return ResponseOk(user_serializer.data)

    @action(detail=False, methods=['put'], name='edit_my_profile',
            permission_classes=[IsAuthenticated]
            )
    def edit_my_profile(self, request):
        """
        change profile of the current user
        """

        user_serializer = UserSerializer(request.user, data=request.data, partial=True)
        # user_serializer = UserSerializer(User.objects.get(pk=1), data=request.data, partial=True)

        if user_serializer.is_valid():
            user_serializer.save()
            return ResponseOk(user_serializer.data)
        else:
            return ResponseBadRequest(user_serializer.errors)
