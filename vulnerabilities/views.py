from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Vulnerability, FixedVulnerability
from .serializers import VulnerabilitySerializer, FixedVulnerabilitySerializer
import requests

class NistVulnerabilitiesView(APIView):
    def get(self, request):
        url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        
        params = {
            "startIndex": 0,
            "resultsPerPage": 10  # Puedes ajustar este valor
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return Response(data)
        else:
            return Response({"error": "No se pudo obtener la información del NIST"}, status=500)
        
class UnfixedVulnerabilitiesView(APIView):
    def get(self, request):
        # URL del API de NIST
        NIST_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        
        try:
            response = requests.get(NIST_API_URL, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Obtener las vulnerabilidades fixeadas en la BD
            fixed_cves = set(FixedVulnerability.objects.values_list("cve_id", flat=True))
            
            # Filtrar las vulnerabilidades excluyendo las fixeadas
            unfixed_vulnerabilities = [
                vuln for vuln in data.get("vulnerabilities", [])
                if vuln["cve"]["id"] not in fixed_cves
            ]
            
            return Response({"vulnerabilities": unfixed_vulnerabilities}, status=status.HTTP_200_OK)
        
        except requests.RequestException as e:
            return Response({"error": "Error al obtener datos del NIST", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VulnerabilitySummaryView(APIView):
    def get(self, request):
        # Contamos las vulnerabilidades según la severidad
        summary = {
            "low": Vulnerability.objects.filter(severity="Low").count(),
            "medium": Vulnerability.objects.filter(severity="Medium").count(),
            "high": Vulnerability.objects.filter(severity="High").count(),
            "critical": Vulnerability.objects.filter(severity="Critical").count(),
        }
        return Response(summary, status=status.HTTP_200_OK)
    
# Endpoint para listar todas las vulnerabilidades
class VulnerabilityViewSet(viewsets.ModelViewSet):
    queryset = Vulnerability.objects.all()
    serializer_class = VulnerabilitySerializer

# Endpoint para agregar vulnerabilidades corregidas
class FixedVulnerabilityViewSet(viewsets.ModelViewSet):
    queryset = FixedVulnerability.objects.all()
    serializer_class = FixedVulnerabilitySerializer

class VulnerabilityListView(generics.ListAPIView):
    queryset = Vulnerability.objects.all()
    serializer_class = VulnerabilitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['severity', 'status']

# Endpoint para listar solo las vulnerabilidades NO corregidas
@api_view(['GET'])
def list_unfixed_vulnerabilities(request):
    fixed_cve_ids = FixedVulnerability.objects.values_list('cve_id', flat=True)
    unfixed_vulnerabilities = Vulnerability.objects.exclude(cve_id__in=fixed_cve_ids)
    serializer = VulnerabilitySerializer(unfixed_vulnerabilities, many=True)
    return Response(serializer.data)

# Endpoint para obtener un resumen de vulnerabilidades por severidad
@api_view(['GET'])
def vulnerabilities_summary(request):
    summary = Vulnerability.objects.values('severity').annotate(count=Count('id'))
    return Response(summary)

@api_view(['POST'])
def add_fixed_vulnerabilities(request):
    """
    Recibe una lista de CVEs fixeados y los guarda en la base de datos.
    """
    serializer = FixedVulnerabilitySerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def vulnerability_list(request):
    vulnerabilities = Vulnerability.objects.all()
    serializer = VulnerabilitySerializer(vulnerabilities, many=True)
    return Response(serializer.data)

# Endpoint para verificar que la API funciona
def index(request):
    return JsonResponse({'message': 'API de Vulnerabilities funcionando'})


# Create your views here.
