from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    firstname = forms.CharField(max_length=30, required=True, label="Prénom")
    lastname = forms.CharField(max_length=30, required=True, label="Nom")
    email = forms.EmailField(required=True, label="Email")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('firstname', 'lastname', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["firstname"]
        user.last_name = self.cleaned_data["lastname"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user