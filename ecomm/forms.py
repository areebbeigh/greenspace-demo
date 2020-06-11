from django.forms import ModelForm

from green_space.form_mixins import FormMixin
from ecomm.models import Product


class ProductForm(FormMixin, ModelForm):
    style_attrs = {
        'name': {
            'placeholder': 'Product Name',
            'class': 'form-control',
        },
        'description': {
            'placeholder': 'A cool little description',
            'class': 'form-control',
        },
        'price': {
            'placeholder': 'Don\'t be greedy',
            'class': 'form-control',
        },
        'image': {
            'placeholder': 'Cute little pic for your plant',
            'class': 'custom-file-input'
        }
    }

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image',]

