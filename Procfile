web: gunicorn -w 1 resurfedtools.wsgi --log-level debug
daphne: daphne -b 0.0.0.0 -p 8001 resurfedtools.asgi:channel_layer
worker: python manage.py runworker