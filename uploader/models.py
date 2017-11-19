from django.db import models
from .choices import UploadType, ServerType

# Create your models here.


class Server(models.Model):

    order = models.IntegerField(unique=True, blank=False)
    name = models.CharField(max_length=64, blank=False)
    connection = models.CharField(max_length=10, choices=UploadType.choices, blank=False)
    server_type = models.CharField(max_length=20, choices=ServerType.choices, blank=False)
    username = models.CharField(max_length=64, blank=False)
    password = models.CharField(max_length=64, blank=False)
    host_address = models.CharField(max_length=32, blank=False)
    port = models.IntegerField()
    map_cycle_location = models.CharField(max_length=64)
    map_location = models.CharField(max_length=64)
    home_location = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'