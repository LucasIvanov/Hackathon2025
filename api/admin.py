from django.contrib import admin
from .models import (
    Empresa, Incentivo, ArrecadacaoISS, ArrecadacaoIPTU,
    Contrapartida, Alerta, CalculoImpacto, Auditoria, UsuarioSistema
)

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['cnpj', 'razao_social', 'cnae_descricao', 'bairro', 'porte']
    list_filter = ['porte', 'bairro', 'cnae']
    search_fields = ['cnpj', 'razao_social', 'nome_fantasia']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['razao_social']
    list_per_page = 25

@admin.register(Incentivo)
class IncentivoAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'tipo_incentivo', 'instrumento_legal', 'data_inicio', 'data_fim', 'status']
    list_filter = ['tipo_incentivo', 'status', 'data_inicio']
    search_fields = ['empresa__cnpj', 'empresa__razao_social', 'instrumento_legal']
    date_hierarchy = 'data_inicio'

@admin.register(ArrecadacaoISS)
class ArrecadacaoISSAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'mes_ref', 'valor_iss', 'numero_nfse']
    list_filter = ['mes_ref']
    search_fields = ['empresa__cnpj', 'empresa__razao_social']
    date_hierarchy = 'mes_ref'
    ordering = ['-mes_ref']

@admin.register(ArrecadacaoIPTU)
class ArrecadacaoIPTUAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'ano_ref', 'valor_iptu', 'valor_taxas']
    list_filter = ['ano_ref']
    search_fields = ['empresa__cnpj', 'empresa__razao_social']
    ordering = ['-ano_ref']

@admin.register(Contrapartida)
class ContrapartidaAdmin(admin.ModelAdmin):
    list_display = ['incentivo', 'tipo', 'status', 'data_vencimento', 'data_cumprimento']
    list_filter = ['tipo', 'status', 'data_vencimento']
    search_fields = ['incentivo__empresa__cnpj', 'descricao']

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'tipo_alerta', 'severidade', 'status', 'data_alerta']
    list_filter = ['tipo_alerta', 'severidade', 'status', 'data_alerta']
    search_fields = ['empresa__cnpj', 'empresa__razao_social', 'descricao']
    date_hierarchy = 'data_alerta'
    readonly_fields = ['data_alerta']

@admin.register(CalculoImpacto)
class CalculoImpactoAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'periodo_inicio', 'periodo_fim', 'bc_ratio', 'impacto_liquido', 'calculado_em']
    list_filter = ['periodo_inicio', 'periodo_fim']
    search_fields = ['empresa__cnpj', 'empresa__razao_social']
    readonly_fields = ['calculado_em']
    ordering = ['-bc_ratio']

@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'acao', 'cnpj', 'timestamp', 'ip_address']  # timestamp em vez de created_at
    list_filter = ['acao', 'timestamp']
    search_fields = ['usuario', 'cnpj', 'detalhes']
    date_hierarchy = 'timestamp'
    readonly_fields = ['timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(UsuarioSistema)
class UsuarioSistemaAdmin(admin.ModelAdmin):
    list_display = ['username', 'nome_completo', 'cargo', 'departamento', 'ativo', 'ultimo_login']
    list_filter = ['cargo', 'departamento', 'ativo']
    search_fields = ['username', 'nome_completo', 'email']
    readonly_fields = ['ultimo_login', 'criado_em']
    
    fieldsets = (
        ('Informações de Login', {
            'fields': ('username', 'senha', 'email')
        }),
        ('Dados Pessoais', {
            'fields': ('nome_completo', 'cargo', 'departamento')
        }),
        ('Status', {
            'fields': ('ativo', 'ultimo_login', 'criado_em')
        })
    )

# Customizar admin site
admin.site.site_header = "Sistema de Incentivos Fiscais - SEMDEC"
admin.site.site_title = "Incentivos Fiscais Admin"
admin.site.index_title = "Administração do Sistema"
