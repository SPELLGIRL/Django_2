from mainapp.models import Category
from django.forms import ModelForm
from django import forms


class CategoryEditForm(ModelForm):
    discount = forms.IntegerField(label='скидка', required=False, min_value=0,
                                  max_value=90, initial=0)

    class Meta:
        model = Category
        # fields = '__all__'
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
