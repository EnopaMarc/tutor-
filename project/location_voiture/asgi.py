"""
ASGI config for Location de Voiture project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'location_voiture.settings')

application = get_asgi_application()