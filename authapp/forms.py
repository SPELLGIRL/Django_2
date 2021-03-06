from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, \
    UserChangeForm

from django import forms

from .models import CustomUser
from .models import CustomUserProfile

import random
import hashlib


class MyClearableFileInput(forms.ClearableFileInput):
    initial_text = ''
    template_name = 'authapp/widgets/MyClearableFileInput.html'


class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'password1',
            'password2',
            'email',
            'age',
            'avatar'
        )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError(
                "Регистрация доступна для пользователей старше 18 лет!")
        return data

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)

        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[
               :6]
        user.activation_key = hashlib.sha1(
            (user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user


class UpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'age',
            'avatar',
            'password'
        )
        widgets = {
            'avatar': MyClearableFileInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 14:
            raise forms.ValidationError(
                "Ресурс доступен толеео для пользователей старше 14 лет!")
        return data


class CustomUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUserProfile
        fields = ('tagline', 'aboutMe', 'gender')

    def __init__(self, *args, **kwargs):
        super(CustomUserProfileEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
