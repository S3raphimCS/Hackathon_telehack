import random
from string import ascii_letters, digits

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import CustomUser


@api_view(["GET"])
def me(request):
    """Функция возвращает информацию о пользователе для отображения в углу страницы."""
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


def create_random_password(pass_len):
    """Функция для создания случайного надежного пароля для пользователя."""
    characters = ascii_letters + digits
    new_password = ''.join(random.choice(characters) for _ in range(pass_len))
    return new_password


@swagger_auto_schema(
    method='POST',
    operation_description=_("Создание пользователя"),
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required="__all__",
        properties={
            "email": openapi.Schema(type=openapi.FORMAT_EMAIL, example="admin@mail.ru"),
            "first_name": openapi.Schema(type=openapi.TYPE_STRING, example='Сергей'),
            "last_name": openapi.Schema(type=openapi.TYPE_STRING, example='Задонский'),
            "middle_name": openapi.Schema(type=openapi.TYPE_STRING, example='Сергеевич'),
        }
    )
)
@api_view(["POST"])
def signup_user(request):
    """Создает пользователя и генерирует ему уникальный пароль"""
    data = request.data
    if get_user_model().objects.filter(email=data["email"]):
        return Response({"error": 'Пользователь с такой почтой уже существует'}, status=status.HTTP_400_BAD_REQUEST)
    password = create_random_password(15)
    user = CustomUser(email=data["email"].value(),
                      first_name=data["first_name"].value(),
                      last_name=data["last_name"].value(),
                      middle_name=data["middle_name"].value())
    user.set_password(password)
    user.save()
    return Response(
        {
            "data": "Пользователь успешно создан",
            'email': data["email"],
            'password': password,
        },
        status=status.HTTP_201_CREATED)
