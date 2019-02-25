from authapp.models import CustomUser
from django.forms import ModelForm


class UserEditForm(ModelForm):
    class Meta:
        model = CustomUser

        exclude = (
            'id',
            'password',
            'groups',
            'user_permissions',
            'is_staff',
        )

    def __init__(self, *args, **kwargs):
        readonly_fields = (
            'last_login',
            'date_joined'
        )
        super(UserEditForm, self).__init__(*args, **kwargs)
        for field in readonly_fields:
            self.fields[field].widget.attrs['readonly'] = True
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
