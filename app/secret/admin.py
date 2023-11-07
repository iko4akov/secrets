from django.contrib import admin

from secret.models import Secret

class SecretModelAdmin(admin.ModelAdmin):
    list_filter = ['name_secret']

admin.site.register(Secret, SecretModelAdmin)
