from django.contrib import admin
from .models import Credential


class CredentialAdmin(admin.ModelAdmin):
    list_display = ('user', 'alpaca_id', 'alpaca_key')


# Register your models here.
admin.site.register(Credential, CredentialAdmin)
