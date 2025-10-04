from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Empresa(models.Model):
    PORTE_CHOICES = [
        ('MEI', 'Microempreendedor Individual'),
        ('ME', 'Microempresa'),
        ('EPP', 'Empresa de Pequeno Porte'),
        ('MEDIA', 'Empresa de Médio Porte'),
        ('GRANDE', 'Empresa de Grande Porte'),
    ]
    
    cnpj = models.CharField(max_length=14, unique=True, db_index=True)
    razao_social = models.CharField(max_length=255)
    nome_fantasia = models.CharField(max_length=255, blank=True, null=True)
    cnae = models.CharField(max_length=10)
    cnae_descricao = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100, default='Cascavel')
    uf = models.CharField(max_length=2, default='PR')
    data_abertura = models.DateField(blank=True, null=True)
    porte = models.CharField(max_length=10, choices=PORTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'empresas'
        ordering = ['razao_social']
    
    def __str__(self):
        return f"{self.cnpj} - {self.razao_social}"


class Incentivo(models.Model):
    TIPO_CHOICES = [
        ('ISENCAO_ISS', 'Isenção de ISS'),
        ('REDUCAO_ISS', 'Redução de ISS'),
        ('ISENCAO_IPTU', 'Isenção de IPTU'),
        ('REDUCAO_IPTU', 'Redução de IPTU'),
        ('ISENCAO_TAXAS', 'Isenção de Taxas'),
        ('TERRENO_GRATUITO', 'Terreno Gratuito'),
        ('MISTO', 'Incentivo Misto'),
    ]
    
    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('SUSPENSO', 'Suspenso'),
        ('VENCIDO', 'Vencido'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='incentivos', to_field='cnpj', db_column='cnpj')
    instrumento_legal = models.CharField(max_length=100)
    tipo_incentivo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    percentual_desconto = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    valor_fixo_desconto = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    contrapartidas = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ATIVO')
    baseline_iss_12m = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    baseline_iptu_12m = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    observacoes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'incentivos'
        ordering = ['-data_inicio']
    
    def __str__(self):
        return f"{self.empresa.cnpj} - {self.get_tipo_incentivo_display()}"


class ArrecadacaoISS(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='arrecadacao_iss', to_field='cnpj', db_column='cnpj')
    mes_ref = models.DateField()
    valor_iss = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_base_calculo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    aliquota = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    numero_nfse = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'arrecadacao_iss'
        unique_together = [['empresa', 'mes_ref']]
        ordering = ['-mes_ref']
    
    def __str__(self):
        return f"{self.empresa.cnpj} - {self.mes_ref.strftime('%m/%Y')}"


class ArrecadacaoIPTU(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='arrecadacao_iptu', to_field='cnpj', db_column='cnpj')
    ano_ref = models.IntegerField()
    valor_iptu = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_taxas = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_alvara = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'arrecadacao_iptu_taxas'
        unique_together = [['empresa', 'ano_ref']]
        ordering = ['-ano_ref']
    
    def __str__(self):
        return f"{self.empresa.cnpj} - {self.ano_ref}"


class Contrapartida(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('EM_ANALISE', 'Em Análise'),
        ('CUMPRIDA', 'Cumprida'),
        ('DESCUMPRIDA', 'Descumprida'),
    ]
    
    TIPO_CHOICES = [
        ('EMPREGOS', 'Geração de Empregos'),
        ('INVESTIMENTO', 'Investimento em Infraestrutura'),
        ('QUALIFICACAO', 'Qualificação Profissional'),
        ('PERMANENCIA', 'Permanência no Município'),
        ('OUTRO', 'Outro'),
    ]
    
    incentivo = models.ForeignKey(Incentivo, on_delete=models.CASCADE, related_name='contrapartidas_detalhadas')
    descricao = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    data_vencimento = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    data_cumprimento = models.DateField(blank=True, null=True)
    observacoes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'contrapartidas'
        ordering = ['data_vencimento']
    
    def __str__(self):
        return f"{self.incentivo.empresa.cnpj} - {self.get_tipo_display()}"


class Alerta(models.Model):
    TIPO_CHOICES = [
        ('BC_BAIXO', 'Relação B/C Abaixo de 1'),
        ('SEM_RECOLHIMENTO', 'Sem Recolhimento'),
        ('CONTRAPARTIDA_VENCENDO', 'Contrapartida Vencendo'),
        ('IMPACTO_NEGATIVO', 'Impacto Líquido Negativo'),
        ('INCENTIVO_VENCENDO', 'Incentivo Vencendo'),
    ]
    
    SEVERIDADE_CHOICES = [
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ]
    
    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('RESOLVIDO', 'Resolvido'),
        ('IGNORADO', 'Ignorado'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='alertas', to_field='cnpj', db_column='cnpj')
    tipo_alerta = models.CharField(max_length=30, choices=TIPO_CHOICES)
    descricao = models.TextField()
    severidade = models.CharField(max_length=10, choices=SEVERIDADE_CHOICES, default='MEDIA')
    data_alerta = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ATIVO')
    resolvido_em = models.DateTimeField(blank=True, null=True)
    resolvido_por = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='alertas_resolvidos')
    observacoes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'alertas'
        ordering = ['-data_alerta', '-severidade']
    
    def __str__(self):
        return f"{self.get_tipo_alerta_display()} - {self.empresa.cnpj}"


class CalculoImpacto(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='calculos', to_field='cnpj', db_column='cnpj')
    periodo_inicio = models.DateField()
    periodo_fim = models.DateField()
    custo_fiscal = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    arrecadacao_incremental = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    impacto_liquido = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    bc_ratio = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    payback_meses = models.IntegerField(blank=True, null=True)
    calculado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'calculos_impacto'
        unique_together = [['empresa', 'periodo_inicio', 'periodo_fim']]
        ordering = ['-calculado_em']
    
    def __str__(self):
        return f"{self.empresa.cnpj} - B/C: {self.bc_ratio}"


class Auditoria(models.Model):
    ACAO_CHOICES = [
        ('CONSULTA', 'Consulta'),
        ('UPLOAD', 'Upload de Dados'),
        ('CALCULO', 'Cálculo Realizado'),
        ('EXPORTACAO', 'Exportação de Relatório'),
        ('ALTERACAO', 'Alteração de Dados'),
        ('EXCLUSAO', 'Exclusão de Dados'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    acao = models.CharField(max_length=20, choices=ACAO_CHOICES)
    tabela = models.CharField(max_length=50, blank=True)
    registro_id = models.IntegerField(blank=True, null=True)
    cnpj = models.CharField(max_length=14, blank=True)
    detalhes = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'auditoria'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.usuario} - {self.get_acao_display()}"
