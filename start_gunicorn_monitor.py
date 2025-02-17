import subprocess
import time
import os

def start_gunicorn():
    # Define your Gunicorn command and options
    gunicorn_command = [
        "/home/container/.local/bin/gunicorn",  # Make sure to use correct path to Gunicorn
        "--workers", "3",                      # Number of workers
        "--bind", "0.0.0.0:26071",            # Binding to address and port
        "--worker-class", "gthread",          # Worker class for better performance
        "--reload",                           # Enable reloading for development (remove for production)
        "--reload-extra-file=wydm_app/templates/",
        "--reload-extra-file=wydm_app/static/css/",
        "--reload-extra-file=wydm_app/static/js/",
        "wydm_project.wsgi:application"       # Path to your WSGI application
    ]
    
    process = subprocess.Popen(
        gunicorn_command, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )

    return process

def monitor_gunicorn():
    while True:
        process = start_gunicorn()
        print("🚀 Gunicorn started successfully!")

        while True:
            time.sleep(10)  # Check every 10 seconds

            # Check if Gunicorn process has finished (stopped or failed)
            if process.poll() is not None:
                # Capture and print Gunicorn output if it stops
                stdout, stderr = process.communicate()
                print("⚠️ Gunicorn stopped. Restarting...")

                if stdout:
                    print("Gunicorn stdout:\n", stdout.decode())
                if stderr:
                    print("Gunicorn stderr:\n", stderr.decode())

                break  # Restart Gunicorn by exiting inner loop

if __name__ == "__main__":
    monitor_gunicorn()
