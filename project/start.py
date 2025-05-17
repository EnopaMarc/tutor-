"""
Script de démarrage pour initialiser la base de données avec des exemples de voitures.
"""
import os
import django
import random
from datetime import date, timedelta

# Configurer l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'location_voiture.settings')
django.setup()

# Importer les modèles après la configuration de Django
from django.contrib.auth.models import User
from rental.models import Voiture, Location

def create_superuser():
    """Crée un superutilisateur s'il n'existe pas déjà."""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        print('Superutilisateur créé: admin / adminpass')
    else:
        print('Le superutilisateur existe déjà')

def create_sample_cars():
    """Crée des exemples de voitures s'il n'y en a pas déjà."""
    if Voiture.objects.count() == 0:
        # Voitures tout-terrain
        tout_terrains = [
            {
                'marque': 'Jeep', 
                'modele': 'Wrangler', 
                'annee': 2023, 
                'type': 'TT', 
                'prix_journalier': 95.00,
                'description': 'Parfait pour l\'aventure et l\'exploration hors route. Ce Jeep Wrangler est équipé pour affronter tous les terrains avec sa transmission intégrale et sa garde au sol élevée.'
            },
            {
                'marque': 'Toyota', 
                'modele': 'Land Cruiser', 
                'annee': 2022, 
                'type': 'TT', 
                'prix_journalier': 120.00,
                'description': 'Le Toyota Land Cruiser allie robustesse et fiabilité légendaire. Idéal pour les longs trajets sur routes difficiles et l\'aventure en montagne.'
            },
            {
                'marque': 'Land Rover', 
                'modele': 'Defender', 
                'annee': 2023, 
                'type': 'TT', 
                'prix_journalier': 135.00,
                'description': 'Le nouveau Land Rover Defender combine performances tout-terrain exceptionnelles et confort moderne. Un véhicule iconique pour toutes vos aventures.'
            },
            {
                'marque': 'Ford', 
                'modele': 'Bronco', 
                'annee': 2022, 
                'type': 'TT', 
                'prix_journalier': 90.00,
                'description': 'Le Ford Bronco est de retour! Ce 4x4 combine style rétro et technologies modernes pour des performances tout-terrain impressionnantes.'
            },
            {
                'marque': 'Nissan', 
                'modele': 'Patrol', 
                'annee': 2021, 
                'type': 'TT', 
                'prix_journalier': 110.00,
                'description': 'Le Nissan Patrol est un SUV tout-terrain spacieux et puissant, parfait pour les familles aventureuses qui ont besoin d\'espace et de capacités hors route.'
            }
        ]
        
        # Voitures familiales
        familiales = [
            {
                'marque': 'Renault', 
                'modele': 'Espace', 
                'annee': 2022, 
                'type': 'FM', 
                'prix_journalier': 75.00,
                'description': 'Le Renault Espace est un monospace spacieux et confortable, idéal pour les voyages en famille. 7 places et un grand coffre pour tous vos bagages.'
            },
            {
                'marque': 'Volkswagen', 
                'modele': 'Passat SW', 
                'annee': 2023, 
                'type': 'FM', 
                'prix_journalier': 65.00,
                'description': 'Cette Volkswagen Passat SW combine espace, confort et plaisir de conduite. Son grand coffre et son équipement complet en font le compagnon idéal pour les longs trajets.'
            },
            {
                'marque': 'Peugeot', 
                'modele': '5008', 
                'annee': 2022, 
                'type': 'FM', 
                'prix_journalier': 70.00,
                'description': 'Le Peugeot 5008 est un SUV familial 7 places au design élégant et à l\'équipement technologique complet. Parfait pour les familles modernes.'
            },
            {
                'marque': 'Citroën', 
                'modele': 'Grand C4 SpaceTourer', 
                'annee': 2021, 
                'type': 'FM', 
                'prix_journalier': 60.00,
                'description': 'Le Citroën Grand C4 SpaceTourer offre un espace intérieur généreux et une modularité exceptionnelle. Idéal pour les familles nombreuses.'
            },
            {
                'marque': 'BMW', 
                'modele': 'Série 5 Touring', 
                'annee': 2023, 
                'type': 'FM', 
                'prix_journalier': 95.00,
                'description': 'La BMW Série 5 Touring allie le plaisir de conduite BMW au côté pratique d\'un break. Luxe, confort et espace pour toute la famille.'
            },
            {
                'marque': 'Skoda', 
                'modele': 'Kodiaq', 
                'annee': 2022, 
                'type': 'FM', 
                'prix_journalier': 65.00,
                'description': 'Le Skoda Kodiaq est un SUV familial 7 places qui offre un excellent rapport qualité-prix. Spacieux, bien équipé et fiable.'
            }
        ]
        
        # Créer les voitures
        for car_data in tout_terrains + familiales:
            Voiture.objects.create(**car_data)
        
        print(f'Créé {len(tout_terrains)} voitures tout-terrain et {len(familiales)} voitures familiales')
    else:
        print('Des voitures existent déjà dans la base de données')

def create_sample_users():
    """Crée des utilisateurs de test s'ils n'existent pas déjà."""
    if User.objects.count() <= 1:  # On compte l'admin
        users = [
            {'username': 'jean', 'email': 'jean@example.com', 'password': 'test1234', 'first_name': 'Jean', 'last_name': 'Dupont'},
            {'username': 'marie', 'email': 'marie@example.com', 'password': 'test1234', 'first_name': 'Marie', 'last_name': 'Martin'},
            {'username': 'pierre', 'email': 'pierre@example.com', 'password': 'test1234', 'first_name': 'Pierre', 'last_name': 'Bernard'}
        ]
        
        for user_data in users:
            if not User.objects.filter(username=user_data['username']).exists():
                User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )
        
        print(f'Créé {len(users)} utilisateurs de test')
    else:
        print('Des utilisateurs existent déjà dans la base de données')

def create_sample_rentals():
    """Crée des exemples de locations s'il n'y en a pas déjà."""
    if Location.objects.count() == 0 and User.objects.count() > 1 and Voiture.objects.count() > 0:
        users = User.objects.exclude(username='admin')
        voitures = list(Voiture.objects.all())
        
        # Statuts possibles
        statuts = [
            Location.StatutLocation.EN_ATTENTE,
            Location.StatutLocation.EN_COURS,
            Location.StatutLocation.TERMINE,
            Location.StatutLocation.ANNULE
        ]
        
        # Créer quelques locations
        for i in range(min(10, len(voitures))):
            user = random.choice(users)
            voiture = voitures[i]
            
            # Dates aléatoires
            today = date.today()
            start_days = random.randint(-30, 30)  # Date entre -30 et +30 jours
            duration = random.randint(1, 10)  # Durée entre 1 et 10 jours
            
            date_debut = today + timedelta(days=start_days)
            date_fin = date_debut + timedelta(days=duration)
            
            # Statut en fonction des dates
            if date_debut > today:
                statut = Location.StatutLocation.EN_ATTENTE
            elif date_fin < today:
                statut = random.choice([Location.StatutLocation.TERMINE, Location.StatutLocation.ANNULE])
            else:
                statut = Location.StatutLocation.EN_COURS
            
            # Si location en cours, la voiture n'est pas disponible
            if statut == Location.StatutLocation.EN_COURS:
                voiture.disponible = False
                voiture.save()
            
            # Créer la location
            location = Location(
                utilisateur=user,
                voiture=voiture,
                date_debut=date_debut,
                date_fin=date_fin,
                statut=statut
            )
            
            # Calculer le montant
            location.save()  # Sauvegarde pour déclencher le calcul du montant
            
            # Si statut autre que EN_ATTENTE, simuler un paiement
            if statut != Location.StatutLocation.EN_ATTENTE:
                location.paiement_id = f"pi_test_{random.randint(10000, 99999)}"
                location.save()
        
        print(f'Créé {min(10, len(voitures))} exemples de locations')
    else:
        print('Des locations existent déjà ou il manque des utilisateurs/voitures')

if __name__ == '__main__':
    print('Initialisation de la base de données...')
    create_superuser()
    create_sample_cars()
    create_sample_users()
    create_sample_rentals()
    print('Initialisation terminée !')
    print('Démarrage du serveur Django...')
    os.system('python manage.py runserver 0.0.0.0:3000')