"""
Modèles pour l'application de location de voitures.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Voiture(models.Model):
    """Modèle représentant une voiture disponible à la location."""
    
    class TypeVoiture(models.TextChoices):
        TOUT_TERRAIN = 'TT', _('Tout-terrain')
        FAMILIALE = 'FM', _('Familiale')
    
    type = models.CharField(
        max_length=2,
        choices=TypeVoiture.choices,
        default=TypeVoiture.FAMILIALE,
        verbose_name="Type de véhicule"
    )
    marque = models.CharField(max_length=100, verbose_name="Marque")
    modele = models.CharField(max_length=100, verbose_name="Modèle")
    annee = models.IntegerField(verbose_name="Année")
    disponible = models.BooleanField(default=True, verbose_name="Disponible")
    prix_journalier = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Prix journalier (€)")
    image = models.ImageField(upload_to='voitures/', null=True, blank=True, verbose_name="Image")
    description = models.TextField(blank=True, verbose_name="Description")
    
    def __str__(self):
        return f"{self.marque} {self.modele} ({self.annee})"
    
    class Meta:
        verbose_name = "Voiture"
        verbose_name_plural = "Voitures"

class Location(models.Model):
    """Modèle représentant une location de voiture."""
    
    class StatutLocation(models.TextChoices):
        EN_ATTENTE = 'AT', _('En attente de paiement')
        EN_COURS = 'EC', _('En cours')
        TERMINE = 'TR', _('Terminé')
        ANNULE = 'AN', _('Annulé')
    
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locations', verbose_name="Utilisateur")
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE, related_name='locations', verbose_name="Voiture")
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(verbose_name="Date de fin")
    statut = models.CharField(
        max_length=2,
        choices=StatutLocation.choices,
        default=StatutLocation.EN_ATTENTE,
        verbose_name="Statut"
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    paiement_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="ID de paiement")
    montant_total = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Montant total (€)")
    
    def __str__(self):
        return f"Location de {self.voiture} par {self.utilisateur.username} ({self.get_statut_display()})"
    
    def calculer_montant(self):
        """Calcule le montant total de la location."""
        import datetime
        delta = (self.date_fin - self.date_debut).days + 1
        return self.voiture.prix_journalier * delta
    
    def save(self, *args, **kwargs):
        if not self.montant_total:
            self.montant_total = self.calculer_montant()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ['-date_creation']