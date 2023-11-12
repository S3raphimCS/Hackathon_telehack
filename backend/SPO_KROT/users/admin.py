from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import path
from rest_framework.decorators import api_view

from .forms import UserSignUpForm
from .models import CustomUser
from .views import create_random_password


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    change_list_template = 'articles/model_change_list.html'

    def get_urls(self):
        urls = super(UserAdmin, self).get_urls()

        custom_urls = [path('create/', self.signup, name='create_new_user')]
        return custom_urls + urls

    @api_view(["POST"])
    def signup(self):
        form = UserSignUpForm(data=self.POST)
        if form.is_valid():
            password = create_random_password(15)
            get_user_model().objects.create(email=form["email"].value(), first_name=form["first_name"].value(),
                                            last_name=form["last_name"].value(),
                                            middle_name=form["middle_name"].value(),
                                            password=password)
            return HttpResponseRedirect('../../../../admin/users/customuser',
                                        {"messages": messages.success(self,
                                                                      f"Пользователь успешно добавлен\n"
                                                                      f"Логин: {form['email'].value()}\n"
                                                                      f"Пароль: {password}")})
        return HttpResponseRedirect("../../../../admin/users/customuser",
                                    {"messages": messages.error(self,
                                                                'Форма не прошла валидацию. Проверьте, '
                                                                'не ошиблись ли вы в почте, '
                                                                'либо нет ли зарегистрированного пользователя '
                                                                'с такой почтой')})

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
