from django.contrib import admin
from .models import Server, ConnectionInfo
from django.contrib.contenttypes.admin import GenericTabularInline


# Register your models here.

class ConnectInfoInline(admin.StackedInline):
    model = ConnectionInfo


class ServerAdmin(admin.ModelAdmin):
    inlines = [
        ConnectInfoInline,
    ]


admin.site.register(Server, ServerAdmin)
