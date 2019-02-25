from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, \
    UserChangeForm

from django import forms

from authapp.models import CustomUser


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
        if data < 14:
            raise forms.ValidationError(
                "Регистрация доступна для пользователей старше 14 лет!")
        return data


class UpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'email',
            'age',
            'avatar',
            'password'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'input-form__single-input'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 14:
            raise forms.ValidationError(
                "Ресурс доступен толеео для пользователей старше 14 лет!")
        return data
