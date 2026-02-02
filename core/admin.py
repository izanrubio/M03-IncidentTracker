# core/admin.py
from django.contrib import admin
from .models import SecurityIncident

@admin.register(SecurityIncident)
class SecurityIncidentAdmin(admin.ModelAdmin):
    list_display = ('title', 'severity', 'detected_at')