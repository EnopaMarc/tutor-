"""
Vues pour l'application de location de voitures.
"""
import stripe
from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from .models import Voiture, Location
from .forms import CustomUserCreationForm, LocationForm, PaiementForm, RechercheVoitureForm

# Configuration de Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    """Page d'accueil avec liste des voitures disponibles et recherche."""
    form = RechercheVoitureForm(request.GET or None)
    voitures = Voiture.objects.all()
    
    if form.is_valid():
        if form.cleaned_data['type']:
            voitures = voitures.filter(type=form.cleaned_data['type'])
        if form.cleaned_data['marque']:
            voitures = voitures.filter(marque__icontains=form.cleaned_data['marque'])
        if form.cleaned_data['disponible']:
            voitures = voitures.filter(disponible=True)
    
    # Récupérer les voitures tout-terrain et familiales pour la page d'accueil
    tout_terrains = Voiture.objects.filter(type=Voiture.TypeVoiture.TOUT_TERRAIN, disponible=True)[:4]
    familiales = Voiture.objects.filter(type=Voiture.TypeVoiture.FAMILIALE, disponible=True)[:4]
    
    return render(request, 'rental/home.html', {
        'form': form,
        'voitures': voitures,
        'tout_terrains': tout_terrains,
        'familiales': familiales,
    })

def detail_voiture(request, voiture_id):
    """Affiche les détails d'une voiture et permet de la réserver."""
    voiture = get_object_or_404(Voiture, pk=voiture_id)
    form = None
    
    if request.user.is_authenticated:
        form = LocationForm(request.POST or None)
        
        if form.is_valid():
            location = form.save(commit=False)
            location.utilisateur = request.user
            location.voiture = voiture
            location.save()
            return redirect('paiement', location_id=location.id)
    
    return render(request, 'rental/detail_voiture.html', {
        'voiture': voiture,
        'form': form,
    })

def inscription(request):
    """Inscription d'un nouvel utilisateur."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Votre compte a été créé avec succès !")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/signup.html', {
        'form': form,
    })

@login_required
def paiement(request, location_id):
    """Page de paiement pour une location."""
    location = get_object_or_404(Location, pk=location_id, utilisateur=request.user)
    
    if location.statut != Location.StatutLocation.EN_ATTENTE:
        messages.error(request, "Cette location a déjà été payée ou annulée.")
        return redirect('mes_locations')
    
    form = PaiementForm(request.POST or None)
    
    if form.is_valid():
        # Simuler un paiement avec Stripe
        try:
            # Créer un paiement dans Stripe (mode test)
            charge = stripe.PaymentIntent.create(
                amount=int(location.montant_total * 100),  # Stripe utilise les centimes
                currency="eur",
                payment_method_types=["card"],
                description=f"Location de {location.voiture} du {location.date_debut} au {location.date_fin}",
                metadata={"location_id": location.id}
            )
            
            # Mettre à jour la location
            location.paiement_id = charge.id
            location.statut = Location.StatutLocation.EN_COURS
            location.save()
            
            # Marquer la voiture comme indisponible
            voiture = location.voiture
            voiture.disponible = False
            voiture.save()
            
            messages.success(request, "Paiement effectué avec succès !")
            return redirect('confirmation', location_id=location.id)
        
        except Exception as e:
            messages.error(request, f"Erreur lors du paiement: {str(e)}")
    
    return render(request, 'rental/paiement.html', {
        'form': form,
        'location': location,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })

@login_required
def confirmation(request, location_id):
    """Page de confirmation après un paiement réussi."""
    location = get_object_or_404(Location, pk=location_id, utilisateur=request.user)
    return render(request, 'rental/confirmation.html', {
        'location': location,
    })

@login_required
def mes_locations(request):
    """Affiche les locations de l'utilisateur connecté."""
    locations = Location.objects.filter(utilisateur=request.user).order_by('-date_creation')
    return render(request, 'rental/mes_locations.html', {
        'locations': locations,
    })

@login_required
def annuler_location(request, location_id):
    """Annule une location en attente de paiement."""
    location = get_object_or_404(Location, pk=location_id, utilisateur=request.user)
    
    if location.statut == Location.StatutLocation.EN_ATTENTE:
        location.statut = Location.StatutLocation.ANNULE
        location.save()
        messages.success(request, "La location a été annulée.")
    else:
        messages.error(request, "Impossible d'annuler cette location.")
    
    return redirect('mes_locations')