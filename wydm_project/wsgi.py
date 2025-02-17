import os
import subprocess
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "serenade_project.settings")

# Start Gunicorn automatically (if not already running)
try:
    subprocess.Popen([
        "gunicorn",
        "--workers", "3",
        "--bind", "0.0.0.0:8000",
        "--worker-class", "gthread",  # Efficient file watching
        "--reload", 
        "--reload-extra-file=templates/",
        "--reload-extra-file=static/css/",
        "--reload-extra-file=static/js/",
        "serenade_project.wsgi:application"
    ])
    print("🚀 Gunicorn started automatically with watchfiles!")
except Exception as e:
    print(f"⚠️ Gunicorn failed to start: {e}")

# Initialize the WSGI application
application = get_wsgi_application()

# Enable WhiteNoise for serving static files
application = WhiteNoise(application, root="/home/container/staticfiles")
