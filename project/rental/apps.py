"""
Configuration de l'application de location de voitures.
"""
from django.apps import AppConfig

class RentalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rental'
    verbose_name = "Location de Voitures"