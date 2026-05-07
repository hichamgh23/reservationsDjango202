"""
forms.py — Formulaires Django de l'application catalogue

Formulaires disponibles :
    - SignUpForm     : inscription utilisateur
    - ArtistForm     : création / modification d'un artiste
    - LocalityForm   : création / modification d'une localité
    - ReviewForm     : dépôt d'un avis sur un spectacle
"""

from django import forms
from django.contrib.auth.models import User

from .models import Artist, Locality, Review


# ─────────────────────────────────────────────
# AUTHENTIFICATION
# ─────────────────────────────────────────────

class SignUpForm(forms.ModelForm):
    """Formulaire d'inscription avec confirmation de mot de passe et choix de langue."""

    first_name = forms.CharField(max_length=30, required=True, label="Prénom")
    last_name  = forms.CharField(max_length=30, required=True, label="Nom")
    email      = forms.EmailField(required=True, label="Email")

    LANGUAGES = [
        ('fr', 'Français'),
        ('nl', 'Néerlandais'),
        ('en', 'Anglais'),
    ]
    language = forms.ChoiceField(choices=LANGUAGES, label="Langue")

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Mot de passe",
        help_text="Min. 6 caractères, une majuscule et un caractère spécial.",
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirmer le mot de passe",
    )

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        """Vérifie que les deux mots de passe sont identiques."""
        cleaned_data     = super().clean()
        password         = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("La correspondance des mots de passe a échoué.")

        return cleaned_data


# ─────────────────────────────────────────────
# ARTISTES
# ─────────────────────────────────────────────

class ArtistForm(forms.ModelForm):
    """Formulaire de création et modification d'un artiste."""

    class Meta:
        model  = Artist
        fields = ['firstname', 'lastname']
        labels = {
            'firstname': 'Prénom',
            'lastname':  'Nom',
        }


# ─────────────────────────────────────────────
# LOCALITÉS
# ─────────────────────────────────────────────

class LocalityForm(forms.ModelForm):
    """Formulaire de création et modification d'une localité."""

    class Meta:
        model  = Locality
        fields = ['postal_code', 'locality']
        labels = {
            'postal_code': 'Code postal',
            'locality':    'Localité',
        }


# ─────────────────────────────────────────────
# AVIS
# ─────────────────────────────────────────────

class ReviewForm(forms.ModelForm):
    """Formulaire de dépôt d'un avis utilisateur sur un spectacle."""

    class Meta:
        model  = Review
        fields = ['stars', 'review']
        labels = {
            'stars':  'Note (1 à 5)',
            'review': 'Votre commentaire',
        }
        widgets = {
            'stars': forms.NumberInput(attrs={
                'min': 1, 'max': 5, 'class': 'form-control',
            }),
            'review': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Partagez votre avis sur ce spectacle…',
            }),
        }
