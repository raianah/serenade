import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Start Gunicorn with watchfiles for templates and static files"

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Starting Gunicorn with watchfiles...")

        cmd = [
            "gunicorn",
            "--workers", "3",
            "--bind", "0.0.0.0:8000",
            "--worker-class", "gthread",  # For better performance
            "--reload",  # Enables basic reloading
            "--reload-extra-file=templates/",
            "--reload-extra-file=static/css/",
            "--reload-extra-file=static/js/",
            "serenade_project.wsgi:application"
        ]

        subprocess.Popen(cmd)  # Runs in the background
        self.stdout.write("✅ Gunicorn started successfully with auto-reload!")
