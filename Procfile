web: daphne -b 0.0.0.0 -p 5000 resurfedtools.asgi:channel_layer
worker: python manage.py runworker
celery: celery -A resurfedtools worker --loglevel=INFO