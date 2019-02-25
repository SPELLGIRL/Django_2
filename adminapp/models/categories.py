from mainapp.models import Category
from django.forms import ModelForm


class CategoryEditForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
