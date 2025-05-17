"""
Configuration de l'administration pour l'application de location de voitures.
"""
from django.contrib import admin
from .models import Voiture, Location

@admin.register(Voiture)
class VoitureAdmin(admin.ModelAdmin):
    """Interface d'administration pour les voitures."""
    list_display = ('marque', 'modele', 'annee', 'type', 'prix_journalier', 'disponible')
    list_filter = ('type', 'disponible', 'marque')
    search_fields = ('marque', 'modele')
    list_editable = ('disponible', 'prix_journalier')
    fieldsets = (
        ('Informations générales', {
            'fields': ('marque', 'modele', 'annee', 'type', 'description')
        }),
        ('Disponibilité et tarif', {
            'fields': ('disponible', 'prix_journalier')
        }),
        ('Image', {
            'fields': ('image',)
        }),
    )

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Interface d'administration pour les locations."""
    list_display = ('voiture', 'utilisateur', 'date_debut', 'date_fin', 'statut', 'montant_total', 'date_creation')
    list_filter = ('statut', 'date_debut', 'date_creation')
    search_fields = ('utilisateur__username', 'voiture__marque', 'voiture__modele')
    readonly_fields = ('date_creation', 'paiement_id', 'montant_total')
    list_select_related = ('utilisateur', 'voiture')
    date_hierarchy = 'date_creation'
    fieldsets = (
        ('Informations de location', {
            'fields': ('utilisateur', 'voiture', 'date_debut', 'date_fin')
        }),
        ('Statut et paiement', {
            'fields': ('statut', 'montant_total', 'paiement_id', 'date_creation')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Met à jour le statut de disponibilité de la voiture lors de changements."""
        ancien_statut = None
        if change:
            ancien_statut = Location.objects.get(pk=obj.pk).statut
        
        super().save_model(request, obj, form, change)
        
        # Si le statut change, mettre à jour la disponibilité de la voiture
        if change and ancien_statut != obj.statut:
            voiture = obj.voiture
            if obj.statut == Location.StatutLocation.EN_COURS:
                voiture.disponible = False
            elif obj.statut == Location.StatutLocation.TERMINE or obj.statut == Location.StatutLocation.ANNULE:
                voiture.disponible = True
            voiture.save()