# backend/api/calculadora.py - Versão Otimizada
from decimal import Decimal
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from .models import Incentivo, ArrecadacaoISS, ArrecadacaoIPTU, CalculoImpacto

class CalculadoraImpactoFiscal:
    """Classe para cálculos de impacto fiscal otimizada"""
    
    def __init__(self, cnpj):
        self.cnpj = cnpj
        self._incentivo = None
        self._empresa = None
    
    @property
    def incentivo(self):
        """Cache do incentivo para evitar múltiplas queries"""
        if not self._incentivo:
            from .models import Incentivo
            self._incentivo = Incentivo.objects.select_related('empresa').filter(
                empresa__cnpj=self.cnpj, 
                status='ATIVO'
            ).first()
        return self._incentivo
    
    @property
    def empresa(self):
        """Cache da empresa"""
        if not self._empresa:
            from .models import Empresa
            self._empresa = Empresa.objects.get(cnpj=self.cnpj)
        return self._empresa
    
    def calcular_custo_fiscal(self, periodo_inicio, periodo_fim):
        """Calcula o Custo Fiscal (CF) - renúncia fiscal total"""
        if not self.incentivo:
            return Decimal('0.00')
        
        custo_total = Decimal('0.00')
        
        # Cálculo ISS
        if self._deve_calcular_iss():
            custo_total += self._calcular_custo_iss(periodo_inicio, periodo_fim)
        
        # Cálculo IPTU
        if self._deve_calcular_iptu():
            custo_total += self._calcular_custo_iptu(periodo_inicio, periodo_fim)
        
        return custo_total
    
    def _deve_calcular_iss(self):
        """Verifica se deve calcular ISS"""
        return ('ISS' in self.incentivo.tipo_incentivo or 
                self.incentivo.tipo_incentivo == 'MISTO')
    
    def _deve_calcular_iptu(self):
        """Verifica se deve calcular IPTU"""
        return ('IPTU' in self.incentivo.tipo_incentivo or 
                self.incentivo.tipo_incentivo in ['MISTO', 'TERRENO_GRATUITO'])
    
    def _calcular_custo_iss(self, periodo_inicio, periodo_fim):
        """Calcula custo fiscal específico do ISS"""
        custo_iss = Decimal('0.00')
        
        # Buscar arrecadação ISS no período
        arrecadacao_iss = ArrecadacaoISS.objects.filter(
            empresa__cnpj=self.cnpj,
            mes_ref__gte=periodo_inicio,
            mes_ref__lte=periodo_fim
        ).aggregate(total=Sum('valor_iss'))['total'] or Decimal('0.00')
        
        if self.incentivo.percentual_desconto:
            custo_iss = arrecadacao_iss * (self.incentivo.percentual_desconto / 100)
        elif self.incentivo.valor_fixo_desconto:
            # Calcular número de meses no período
            meses = self._calcular_meses_periodo(periodo_inicio, periodo_fim)
            custo_iss = self.incentivo.valor_fixo_desconto * meses
        
        return custo_iss
    
    def _calcular_custo_iptu(self, periodo_inicio, periodo_fim):
        """Calcula custo fiscal específico do IPTU"""
        custo_iptu = Decimal('0.00')
        
        # Anos no período
        anos = list(range(periodo_inicio.year, periodo_fim.year + 1))
        
        for ano in anos:
            arrecadacao_ano = ArrecadacaoIPTU.objects.filter(
                empresa__cnpj=self.cnpj,
                ano_ref=ano
            ).aggregate(
                total=Sum('valor_iptu') + Sum('valor_taxas') + Sum('valor_alvara')
            )['total'] or Decimal('0.00')
            
            if self.incentivo.percentual_desconto:
                custo_iptu += arrecadacao_ano * (self.incentivo.percentual_desconto / 100)
        
        return custo_iptu
    
    def calcular_arrecadacao_incremental(self, periodo_inicio, periodo_fim):
        """Calcula Arrecadação Incremental (AI)"""
        if not self.incentivo:
            return Decimal('0.00')
        
        # Baseline (arrecadação 12 meses antes do incentivo)
        baseline_iss = self._calcular_baseline_iss()
        baseline_iptu = self._calcular_baseline_iptu()
        
        # Arrecadação atual no período
        atual_iss = ArrecadacaoISS.objects.filter(
            empresa__cnpj=self.cnpj,
            mes_ref__gte=periodo_inicio,
            mes_ref__lte=periodo_fim
        ).aggregate(total=Sum('valor_iss'))['total'] or Decimal('0.00')
        
        # Projetar baseline para o período atual
        meses_periodo = self._calcular_meses_periodo(periodo_inicio, periodo_fim)
        baseline_projetado = (baseline_iss / 12) * meses_periodo
        
        # Adicionalidade = diferença entre atual e baseline projetado
        adicionalidade = atual_iss - baseline_projetado
        
        # Se adicionalidade for negativa, considerar 0
        return max(adicionalidade, Decimal('0.00'))
    
    def _calcular_baseline_iss(self):
        """Calcula baseline ISS (12 meses antes do incentivo)"""
        if not self.incentivo or not self.incentivo.data_inicio:
            return Decimal('0.00')
        
        # 12 meses antes do início do incentivo
        inicio_baseline = self.incentivo.data_inicio - relativedelta(months=12)
        fim_baseline = self.incentivo.data_inicio - timedelta(days=1)
        
        baseline = ArrecadacaoISS.objects.filter(
            empresa__cnpj=self.cnpj,
            mes_ref__gte=inicio_baseline,
            mes_ref__lte=fim_baseline
        ).aggregate(total=Sum('valor_iss'))['total'] or Decimal('0.00')
        
        return baseline
    
    def _calcular_baseline_iptu(self):
        """Calcula baseline IPTU (anos anteriores)"""
        if not self.incentivo or not self.incentivo.data_inicio:
            return Decimal('0.00')
        
        ano_incentivo = self.incentivo.data_inicio.year
        anos_baseline = [ano_incentivo - 2, ano_incentivo - 1]
        
        baseline = ArrecadacaoIPTU.objects.filter(
            empresa__cnpj=self.cnpj,
            ano_ref__in=anos_baseline
        ).aggregate(
            total=Sum('valor_iptu') + Sum('valor_taxas') + Sum('valor_alvara')
        )['total'] or Decimal('0.00')
        
        # Média dos 2 anos anteriores
        return baseline / 2 if baseline > 0 else Decimal('0.00')
    
    def _calcular_meses_periodo(self, inicio, fim):
        """Calcula número de meses entre duas datas"""
        return (fim.year - inicio.year) * 12 + (fim.month - inicio.month) + 1
    
    def _calcular_payback(self, custo_fiscal, arrecadacao_incremental, periodo_inicio, periodo_fim):
        """Calcula tempo de payback em meses"""
        if arrecadacao_incremental <= 0:
            return None
        
        # Arrecadação incremental mensal média
        meses_periodo = self._calcular_meses_periodo(periodo_inicio, periodo_fim)
        arrecadacao_mensal = arrecadacao_incremental / meses_periodo
        
        if arrecadacao_mensal <= 0:
            return None
        
        # Payback = Custo Fiscal / Arrecadação Mensal
        payback_meses = custo_fiscal / arrecadacao_mensal
        return int(payback_meses) if payback_meses < 999 else 999
    
    def calcular_impacto_completo(self, periodo_inicio=None, periodo_fim=None):
        """Método principal para cálculo completo de impacto"""
        if not self.incentivo:
            return None
        
        # Definir períodos
        periodo_inicio = periodo_inicio or self.incentivo.data_inicio
        periodo_fim = periodo_fim or datetime.now().date()
        
        # Ajustar período se necessário
        if self.incentivo.data_fim and periodo_fim > self.incentivo.data_fim:
            periodo_fim = self.incentivo.data_fim
        
        # Cálculos principais
        custo_fiscal = self.calcular_custo_fiscal(periodo_inicio, periodo_fim)
        arrecadacao_incremental = self.calcular_arrecadacao_incremental(periodo_inicio, periodo_fim)
        impacto_liquido = arrecadacao_incremental - custo_fiscal
        
        # B/C Ratio
        bc_ratio = (arrecadacao_incremental / custo_fiscal 
                   if custo_fiscal > 0 else Decimal('0.00'))
        
        # Payback
        payback_meses = self._calcular_payback(
            custo_fiscal, arrecadacao_incremental, periodo_inicio, periodo_fim
        )
        
        # Salvar resultado no banco
        calculo, created = CalculoImpacto.objects.update_or_create(
            empresa=self.empresa,
            defaults={
                'periodo_inicio': periodo_inicio,
                'periodo_fim': periodo_fim,
                'custo_fiscal': custo_fiscal,
                'arrecadacao_incremental': arrecadacao_incremental,
                'impacto_liquido': impacto_liquido,
                'bc_ratio': bc_ratio,
                'payback_meses': payback_meses,
                'calculado_em': datetime.now()
            }
        )
        
        return {
            'cnpj': self.cnpj,
            'custo_fiscal': float(custo_fiscal),
            'arrecadacao_incremental': float(arrecadacao_incremental),
            'impacto_liquido': float(impacto_liquido),
            'bc_ratio': float(bc_ratio),
            'payback_meses': payback_meses,
            'periodo_inicio': periodo_inicio,
            'periodo_fim': periodo_fim,
            'calculado_em': calculo.calculado_em
        }
