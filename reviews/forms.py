# reviews.forms.py

from django import forms

from reviews.models import ProductReview


class ProductReviewForm(forms.ModelForm):
    
    """
    Classe de formulaire pour soumettre une nouvelle
    un avis utilisateur
    """

    email = forms.EmailField(
        max_length=150,
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "Votre adresse Email *"
        }),
    )

    content = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "rows": 6,
                "placeholder": "Écrivez votre avis ici."
            }
        ),
    )

    rating = forms.CheckboxSelectMultiple()

    
    class Meta:
        model = ProductReview
        fields = ['rating', 'email', 'content']

    def __init__(self, *args, **kwargs):
        super(ProductReviewForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['rating'].widget.attrs.update({'class': 'form-check-inline custom-select'})
