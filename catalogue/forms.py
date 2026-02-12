from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    # Champs obligatoires demandés par le prof 
    first_name = forms.CharField(max_length=30, required=True, label="Prénom")
    last_name = forms.CharField(max_length=30, required=True, label="Nom")
    email = forms.EmailField(required=True, label="Email")
    
    # Choix de la langue (exigence Chapitre 10) 
    LANGUAGES = [
        ('fr', 'Français'),
        ('nl', 'Néerlandais'),
        ('en', 'Anglais'),
    ]
    language = forms.ChoiceField(choices=LANGUAGES, label="Langue")
    
    # Gestion des mots de passe avec confirmation 
    password = forms.CharField(
        widget=forms.PasswordInput(), 
        label="Mot de passe",
        help_text="Min. 6 caractères, une majuscule et un caractère spécial."
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(), 
        label="Confirmer le mot de passe"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        # Vérification de la correspondance 
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("La correspondance des mots de passe a échoué.")
        
        return cleaned_data