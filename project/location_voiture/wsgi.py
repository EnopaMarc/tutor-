"""
WSGI config for Location de Voiture project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'location_voiture.settings')

application = get_wsgi_application()