"""
URLs pour l'application de location de voitures.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('voiture/<int:voiture_id>/', views.detail_voiture, name='detail_voiture'),
    path('inscription/', views.inscription, name='inscription'),
    path('paiement/<int:location_id>/', views.paiement, name='paiement'),
    path('confirmation/<int:location_id>/', views.confirmation, name='confirmation'),
    path('mes-locations/', views.mes_locations, name='mes_locations'),
    path('annuler-location/<int:location_id>/', views.annuler_location, name='annuler_location'),
]