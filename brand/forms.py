from .models import Brand
from django import forms

class BrandForm(forms.ModelForm):
    class Meta:
        model=Brand
        fields='__all__'