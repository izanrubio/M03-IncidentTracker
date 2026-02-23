from django.db import models
from django.contrib.auth.models import User # Importa el model d'usuaris

class SecurityIncident(models.Model):
    SEVERITY_CHOICES = [
        ('LOW', 'Baixa'),
        ('MEDIUM', 'Mitjana'),
        ('HIGH', 'Alta'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        default='MEDIUM'
    )
    detected_at = models.DateTimeField(auto_now_add=True)

    # AFEGEIX AQUESTA LÍNIA:
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
