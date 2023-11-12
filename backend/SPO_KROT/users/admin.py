from django.contrib import admin
from django.urls import path

from .models import CustomUser
from .views import signup_user
from .forms import UserSignUpForm


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    change_list_template = 'articles/model_change_list.html'

    def get_urls(self):
        urls = super(UserAdmin, self).get_urls()

        custom_urls = [path('create/', self.signup, name='create_new_user')]
        return custom_urls + urls

    def signup(self, request):
        # signup_user(request)
        self.message_user(request, f'Создан новый пользователь')

    fieldsets = (
        ("Основная информация", {'fields': ('email', 'password')}),
        ("ФИО", {'fields': ('first_name', 'last_name', 'middle_name')}),
        ("Информация сотрудника", {'fields': ('department', 'employee_code')}),
        ('Аватар пользователя', {'fields': ('avatar',)}),
        ("Флаги пользователя", {"fields": ('is_superuser', 'is_staff', "is_active")}),
        ("Дата и время регистрации", {'fields': ('date_joined',)}),
        ("Права", {'fields': ('user_permissions', 'groups')}),
    )
    list_filter = ('department',)
    list_display = ('email', 'first_name', 'last_name', 'middle_name', 'department')
    list_per_page = 15
    search_fields = ('email', 'first_name', 'last_name', 'middle_name', 'department', 'employee_code')
    ordering = ('email',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.set_password(obj.password)
        else:
            current_password = CustomUser.objects.get(pk=obj.pk).password
            if obj.password != current_password:
                obj.set_password(obj.password)
        obj.save()
