release: python manage.py db upgrade
web: gunicorn --worker-class eventlet -w 1 --log-file=- ghost:ghost
