from django.shortcuts import render
from rest_framework.viewsets import ViewSet

class UserAccountViewSet(ViewSet):
    """
    Ветка для работы с аккаунтами пользователей.
    """

    serializer_class = UserSerializer

    # @extend_schema(parameters=[UserSerializer])
    @action(detail=False, methods=['post'], name='register')
    def register(self, request):
        """
        Регистрация пользователя
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
        Авторизация пользователей
        """

        auth_form = AuthSerializer(data=request.data)
        if auth_form.is_valid():
            user = authenticate(username=request.data['email'], password=request.data['password'])

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
        Завершить сессию пользователя
        """

        Token.objects.filter(user_id=request.user.id).delete()
        return ResponseOk({'Logout': 'Success'})

    @action(detail=False, methods=['get'], name='my_profile_details',
            permission_classes=[IsAuthenticated]
            )
    def my_profile_details(self, request, *args, **kwargs):
        """
         получить данные моего профиля
        """

        user_serializer = UserSerializer(request.user)
        return ResponseOk(user_serializer.data)

    @action(detail=False, methods=['put'], name='edit_my_profile',
            permission_classes=[IsAuthenticated]
            )
    def edit_my_profile(self, request):
        """
        Изменить данные профиля текущего пользователя
        """

        user_serializer = UserSerializer(request.user, data=request.data, partial=True)
        # user_serializer = UserSerializer(User.objects.get(pk=1), data=request.data, partial=True)

        if user_serializer.is_valid():
            user_serializer.save()
            return ResponseOk(user_serializer.data)
        else:
            return ResponseBadRequest(user_serializer.errors)
