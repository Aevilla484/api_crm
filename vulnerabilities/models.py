from django.db import models
from django.utils.timezone import now

class Vulnerability(models.Model):
    cve_id = models.CharField(max_length=50, unique=True)  # ID de la vulnerabilidad (CVE-XXXX-XXXX)
    description = models.TextField()  # Descripción de la vulnerabilidad
    severity = models.CharField(max_length=20)  # Nivel de severidad (Critical, High, Medium, Low)
    published_date = models.DateTimeField()  # Fecha de publicación
    modified_date = models.DateTimeField()  # Fecha de modificación

    def __str__(self):
        return f"{self.cve_id} - {self.severity}"


class FixedVulnerability(models.Model):
    cve_id = models.CharField(max_length=50, unique=True)
    description = models.TextField(default="No description provided")
    date_fixed = models.DateTimeField(default=now)  # Se asigna la fecha actual por defecto

    def __str__(self):
        return self.cve_id