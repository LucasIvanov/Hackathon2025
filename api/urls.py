# backend/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'empresas', views.EmpresaViewSet)
router.register(r'incentivos', views.IncentivoViewSet)
router.register(r'arrecadacao-iss', views.ArrecadacaoISSViewSet)
router.register(r'arrecadacao-iptu', views.ArrecadacaoIPTUViewSet)
router.register(r'alertas', views.AlertaViewSet)
router.register(r'calculos', views.CalculoImpactoViewSet)
router.register(r'dashboard', views.DashboardViewSet, basename='dashboard')
router.register(r'auditoria', views.AuditoriaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
