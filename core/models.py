from django.db import models

class SecurityIncident(models.Model):
    # Opcions per a la severitat
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

    def __str__(self):
        return self.title