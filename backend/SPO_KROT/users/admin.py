from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
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
