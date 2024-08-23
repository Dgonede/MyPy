from django import forms
from django.forms import ModelForm
from .models import Category


class CategoryCreateUpdateForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def clean_name(self):
        name=self.cleaned_data['name']
        if name.islower():
            raise forms.ValidationError('Only Capital name')
        return name    