"""
Formulaires pour l'application de location de voitures.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Location, Voiture

class CustomUserCreationForm(UserCreationForm):
    """Formulaire d'inscription d'utilisateur personnalisé."""
    email = forms.EmailField(required=True, label="Adresse e-mail")
    first_name = forms.CharField(max_length=30, required=True, label="Prénom")
    last_name = forms.CharField(max_length=30, required=True, label="Nom")
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class LocationForm(forms.ModelForm):
    """Formulaire de location de voiture."""
    date_debut = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date de début",
        initial=timezone.now().date
    )
    date_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date de fin",
        initial=timezone.now().date
    )
    
    class Meta:
        model = Location
        fields = ['date_debut', 'date_fin']
    
    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        
        if date_debut and date_fin:
            if date_debut < timezone.now().date():
                raise forms.ValidationError("La date de début ne peut pas être dans le passé.")
            
            if date_fin < date_debut:
                raise forms.ValidationError("La date de fin doit être postérieure à la date de début.")
        
        return cleaned_data

class PaiementForm(forms.Form):
    """Formulaire de paiement par carte bancaire."""
    MOIS_EXPIRATION = [(i, str(i).zfill(2)) for i in range(1, 13)]
    ANNEES_EXPIRATION = [(i, str(i)) for i in range(timezone.now().year, timezone.now().year + 11)]
    
    nom_carte = forms.CharField(
        max_length=100,
        label="Nom sur la carte",
        widget=forms.TextInput(attrs={'placeholder': 'Jean Dupont'})
    )
    numero_carte = forms.CharField(
        max_length=16,
        min_length=16,
        label="Numéro de carte",
        widget=forms.TextInput(attrs={'placeholder': '4242424242424242'})
    )
    mois_expiration = forms.ChoiceField(
        choices=MOIS_EXPIRATION,
        label="Mois d'expiration"
    )
    annee_expiration = forms.ChoiceField(
        choices=ANNEES_EXPIRATION,
        label="Année d'expiration"
    )
    cvv = forms.CharField(
        max_length=3,
        min_length=3,
        label="CVV",
        widget=forms.TextInput(attrs={'placeholder': '123'})
    )

class RechercheVoitureForm(forms.Form):
    """Formulaire de recherche de voitures."""
    TYPE_CHOICES = [('', 'Tous types')] + list(Voiture.TypeVoiture.choices)
    
    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        required=False,
        label="Type de véhicule"
    )
    marque = forms.CharField(
        max_length=100,
        required=False,
        label="Marque",
        widget=forms.TextInput(attrs={'placeholder': 'Ex: Renault, Peugeot...'})
    )
    disponible = forms.BooleanField(
        required=False,
        label="Uniquement disponibles",
        initial=True
    )