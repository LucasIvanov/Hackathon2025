from django.contrib import admin
from .models import (
    Empresa, Incentivo, ArrecadacaoISS, ArrecadacaoIPTU,
    Contrapartida, Alerta, CalculoImpacto, Auditoria
)


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['cnpj', 'razao_social', 'cnae_descricao', 'bairro', 'porte']
    list_filter = ['porte', 'bairro']
    search_fields = ['cnpj', 'razao_social']


@admin.register(Incentivo)
class IncentivoAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'tipo_incentivo', 'data_inicio', 'status']
    list_filter = ['tipo_incentivo', 'status']


@admin.register(ArrecadacaoISS)
class ArrecadacaoISSAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'mes_ref', 'valor_iss']


@admin.register(ArrecadacaoIPTU)
class ArrecadacaoIPTUAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'ano_ref', 'valor_iptu']


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'tipo_alerta', 'severidade', 'status']
    list_filter = ['tipo_alerta', 'severidade', 'status']


@admin.register(CalculoImpacto)
class CalculoImpactoAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'bc_ratio', 'impacto_liquido']


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'acao', 'cnpj', 'created_at']
    list_filter = ['acao']
