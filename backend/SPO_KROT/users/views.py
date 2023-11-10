import random
import string

from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import api_view
from string import ascii_letters, digits, punctuation


@api_view(["GET"])
def me(request):
    """Функция возвращает информацию о пользователе для отображения в углу страницы"""
    # TODO протестить, что точно не будет анонимных пользователей и убрать
    if request.user.is_anonymous:
        return Response({"user": None})
    user = request.user
    return Response(
        {
            'id': user.id,
            'email': user.email,
            'avatar': user.avatar.name,
            'first_name': user.first_name,
            'second_name': user.last_name,
            'middle_name': user.middle_name,
        }
    )


@swagger_auto_schema(
    method='GET',
    operation_description=_("Создание случайного пароля"),
)
@api_view(["GET"])
def create_random_password(request):
    characters = ascii_letters + digits + punctuation
    new_password = ''.join(random.choice(characters) for _ in range(24))
    return Response({"new_password": new_password})
