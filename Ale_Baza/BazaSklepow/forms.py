from django import forms
from reviews.models import ListaOpinii

class OpinionForm(forms.ModelForm):
    class Meta:
        model = ListaOpinii
        fields = ['opinia']
        widgets = {
            'opinia': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Dodaj swoją opinię...'}),
        }
        labels = {
            'opinia': 'Twoja opinia',
        }
