from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .auth_simple import AuthViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path
from .views import exportar_relatorio_empresas

urlpatterns += [
    path('empresas/exportar/', exportar_relatorio_empresas, name='exportar_relatorio'),
]
