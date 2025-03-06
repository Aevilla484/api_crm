from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VulnerabilityViewSet, 
    FixedVulnerabilityViewSet, 
    index, 
    list_unfixed_vulnerabilities, 
    vulnerabilities_summary,
    add_fixed_vulnerabilities,
    VulnerabilityListView, # Importar la vista
    UnfixedVulnerabilitiesView,
    VulnerabilitySummaryView
)

# Crear router para registrar los viewsets
router = DefaultRouter()
router.register(r'vulnerabilities', VulnerabilityViewSet)
router.register(r'fixed-vulnerabilities', FixedVulnerabilityViewSet)

urlpatterns = [
    path('', index, name='index'),  # Ruta principal para probar la API
    path('', include(router.urls)),  # Rutas generadas por el router
    path('unfixed-vulnerabilities/', list_unfixed_vulnerabilities, name='unfixed_vulnerabilities'),
    path('vulnerabilities-summary/', vulnerabilities_summary, name='vulnerabilities_summary'),
    path('fixed-vulnerabilities/', add_fixed_vulnerabilities, name='add_fixed_vulnerabilities'),
    path('api/fixed-vulnerabilities/', VulnerabilityListView.as_view(), name='fixed-vulnerabilities-list'),
    path("api/unfixed-vulnerabilities/", UnfixedVulnerabilitiesView.as_view(), name="unfixed-vulnerabilities"),
    path('api/vulnerabilities-summary/', VulnerabilitySummaryView.as_view(), name='vulnerabilities_summary'),

]
