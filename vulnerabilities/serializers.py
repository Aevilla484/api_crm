from rest_framework import serializers
from .models import Vulnerability, FixedVulnerability

class VulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vulnerability
        fields = '__all__'  # Serializa todos los campos del modelo

class FixedVulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedVulnerability
        fields = '__all__'  # Serializa todos los campos del modelo

class VulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vulnerability
        fields = '__all__'  # Serializa todos los campos del modelo