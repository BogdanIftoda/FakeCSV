release: python manage.py migrate
web: gunicorn core.wsgi --log-file - 
worker: celery -A core worker -B --loglevel=info