# search.forms.py

from django import forms
from search.models import SearchTerm


class SearchForm(forms.ModelForm):

    """ 
    classe de formulaires pour l'acceptation
    des termes de recherche
    """

    q = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'type': 'search',
                'class': 'form-control',
                'id': 'input-search',
                'placeholder': 'Rechercher un produit, une catégorie, un magasin, une marque...'
            }),
            error_messages={'invalid': 'Veuillez entrer une quantité valide.'},
        )

    class Meta:
        model = SearchTerm
        include = ('q',)
        exclude = ['ip_address', 'date_search_at', 'time_search_at']
