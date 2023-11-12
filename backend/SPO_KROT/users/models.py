from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class MyUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, is_staff=True, is_superuser=True, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password=None, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('first_name', 'Суперпользователь')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('avatar', 'images/users/blank.jpg')
        assert extra_fields['is_staff']
        assert extra_fields['is_superuser']
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    username = None
    objects = MyUserManager()
    avatar = models.ImageField(
        _("Аватар"),
        upload_to="images/users/",
        blank=True, null=True,
        default='images/users/blank.jpg',
    )
    middle_name = models.CharField(
        _('Отчество'),
        max_length=150,
        blank=True
    )
    # TODO Потом это должно быть ForeignKey (Либо можно сделать сразу)
    department = models.CharField(
        _("Название отдела"),
        blank=False, null=True,  # Возможно нужен будет null=False
        max_length=120,
    )
    employee_code = models.CharField(
        _("Код сотрудника"),
        blank=False, null=True,  # Возможно нужен будет null=False
        unique=True,
        max_length=10,
    )
    email = models.EmailField(
        _('Электронная почта'),
        null=True, blank=True,
        default=None,
        unique=True,
        error_messages={
            'unique': _('Указанный адрес уже занят.'),
        },
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.get_full_name()

    def full_name(self):
        """Возвращает полное имя пользователя"""
        names = [self.last_name, self.first_name, self.middle_name]
        full_name = ' '.join(name for name in names if name)
        return full_name.strip()

    def get_full_name(self):
        return self.full_name()
