import subprocess
import os
import sys

os.environ["DJANGO_SETTINGS_MODULE"] = "wydm_project.settings"

# Gunicorn command
gunicorn_command = [
    "/home/container/.local/bin/gunicorn",
    "--workers", "3",
    "--bind", "0.0.0.0:26071",
    "--worker-class", "gthread",
    "--reload-extra-file=wydm_app/templates/",
    "--reload-extra-file=wydm_app/static/css/",
    "--reload-extra-file=wydm_app/static/js/",
    "wydm_project.wsgi:application"
]

try:
    process = subprocess.Popen(gunicorn_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("🚀 Gunicorn started successfully!")

    stdout, stderr = process.communicate()
    if stdout:
        print(stdout.decode())
    if stderr:
        print(stderr.decode(), file=sys.stderr)

except Exception as e:
    print(f"⚠️ Error starting Gunicorn: {e}", file=sys.stderr)
