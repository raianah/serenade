import os
os.system("pkill gunicorn && gunicorn --workers 3 --bind 127.0.0.1:8000 serenade_project.wsgi:application")