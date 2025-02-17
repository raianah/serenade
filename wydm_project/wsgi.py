import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wydm_project.settings")

# Initialize the WSGI application
application = get_wsgi_application()
