from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmpresaViewSet, IncentivoViewSet, ArrecadacaoISSViewSet,
    ArrecadacaoIPTUViewSet, AlertaViewSet, CalculoImpactoViewSet,
    DashboardViewSet
)

router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet)
router.register(r'incentivos', IncentivoViewSet)
router.register(r'arrecadacao-iss', ArrecadacaoISSViewSet)
router.register(r'arrecadacao-iptu', ArrecadacaoIPTUViewSet)
router.register(r'alertas', AlertaViewSet)
router.register(r'calculos-impacto', CalculoImpactoViewSet)
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]
