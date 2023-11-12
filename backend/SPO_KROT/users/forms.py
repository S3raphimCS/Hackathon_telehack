from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm

from .models import CustomUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    class Meta:
        model = CustomUser
        fields = "__all__"

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'last_name', 'first_name', 'middle_name']

        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Эл. Почта",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Фамилия",
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Имя",
            }),
            "middle_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Отчество",
            }),
        }
