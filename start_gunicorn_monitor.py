import subprocess
import time

def start_gunicorn():
    gunicorn_command = [
        "/home/container/.local/bin/gunicorn", # Linux connection
        "--workers", "3",
        "--bind", "0.0.0.0:26071", # Port connected to control.creepercloud.io | Port 2425 for dono-01.danbot.host | Will change everything if relocated
        "--worker-class", "gthread",
        "--reload-extra-file=wydm_app/templates/",
        "--reload-extra-file=wydm_app/static/css/",
        "--reload-extra-file=wydm_app/static/js/",
        "wydm_project.wsgi:application"
    ]
    
    process = subprocess.Popen(gunicorn_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

def monitor_gunicorn():
    while True:
        process = start_gunicorn()
        print("🚀 Gunicorn started successfully!")

        while True:
            time.sleep(10)

            if process.poll() is not None:
                stdout, stderr = process.communicate()
                print("⚠️ Gunicorn stopped. Restarting...")

                # For debugging
                if stdout:
                    print("Gunicorn stdout:\n", stdout.decode())
                if stderr:
                    print("Gunicorn stderr:\n", stderr.decode())

                break

if __name__ == "__main__":
    monitor_gunicorn()
