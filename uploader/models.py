from django.db import models
from .choices import ConnectionType, ServerType


# Create your models here.


class Server(models.Model):
    name = models.CharField(max_length=64, blank=False)
    server_type = models.CharField(max_length=20, choices=ServerType.choices, blank=False)
    map_cycle_location = models.CharField(max_length=64)
    map_location = models.CharField(max_length=64)
    home_location = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class ConnectionInfo(models.Model):
    server = models.OneToOneField(Server, on_delete=models.CASCADE, primary_key=True)
    connection = models.CharField(max_length=10, choices=ConnectionType.choices, blank=False)
    username = models.CharField(max_length=64, blank=False)
    password = models.CharField(max_length=64, blank=False)
    host_address = models.CharField(max_length=32, blank=False)
    port = models.IntegerField()


class UploaderPermissions(models.Model):
    class Meta:
        managed = False

        permissions = (
            ("uploader_access", "Has access to the uploader"),
            ("uploader_admin", "Has uploader admin access")
        )
