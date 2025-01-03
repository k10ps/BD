from django import forms
from .models import ListaProduktow

class ListaProduktowForm(forms.ModelForm):
    class Meta:
        model = ListaProduktow
        fields = ['kategoria', 'marka', 'model']
