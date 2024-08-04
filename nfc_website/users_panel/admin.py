from django.contrib import admin
from .models import nfc_Info

# Register your models here.

class nfcInfoAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'uid_card', 'credit', 'date')

admin.site.register(nfc_Info, nfcInfoAdmin)