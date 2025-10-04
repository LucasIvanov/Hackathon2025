from decimal import Decimal
from datetime import datetime
from django.db.models import Sum
from .models import Incentivo, ArrecadacaoISS, ArrecadacaoIPTU, CalculoImpacto


class CalculadoraImpactoFiscal:
    """Classe para cálculos de impacto fiscal"""
    
    def __init__(self, cnpj):
        self.cnpj = cnpj
        
    def calcular_custo_fiscal(self, incentivo, periodo_inicio, periodo_fim):
        """Calcula o Custo Fiscal (CF) - renúncia fiscal total"""
        custo_total = Decimal('0.00')
        
        if 'ISS' in incentivo.tipo_incentivo or incentivo.tipo_incentivo == 'MISTO':
            iss_periodo = ArrecadacaoISS.objects.filter(
                empresa__cnpj=self.cnpj,
                mes_ref__gte=periodo_inicio,
                mes_ref__lte=periodo_fim
            ).aggregate(total=Sum('valor_iss'))['total'] or Decimal('0.00')
            
            if incentivo.percentual_desconto:
                custo_total += iss_periodo * (incentivo.percentual_desconto / 100)
            elif incentivo.valor_fixo_desconto:
                meses = (periodo_fim.year - periodo_inicio.year) * 12 + (periodo_fim.month - periodo_inicio.month) + 1
                custo_total += incentivo.valor_fixo_desconto * meses
        
        if 'IPTU' in incentivo.tipo_incentivo or incentivo.tipo_incentivo in ['MISTO', 'TERRENO_GRATUITO']:
            iptu_periodo = ArrecadacaoIPTU.objects.filter(
                empresa__cnpj=self.cnpj,
                ano_ref__gte=periodo_inicio.year,
                ano_ref__lte=periodo_fim.year
            ).aggregate(
                total_iptu=Sum('valor_iptu'),
                total_taxas=Sum('valor_taxas')
            )
            
            iptu_total = (iptu_periodo['total_iptu'] or Decimal('0.00')) + (iptu_periodo['total_taxas'] or Decimal('0.00'))
            
            if incentivo.percentual_desconto:
                custo_total += iptu_total * (incentivo.percentual_desconto / 100)
            elif incentivo.valor_fixo_desconto:
                anos = periodo_fim.year - periodo_inicio.year + 1
                custo_total += incentivo.valor_fixo_desconto * anos
        
        return custo_total
    
    def calcular_arrecadacao_incremental(self, incentivo, periodo_inicio, periodo_fim):
        """Calcula a Arrecadação Incremental (AI)"""
        arrecadacao_atual = Decimal('0.00')
        baseline_total = Decimal('0.00')
        
        if 'ISS' in incentivo.tipo_incentivo or incentivo.tipo_incentivo == 'MISTO':
            iss_atual = ArrecadacaoISS.objects.filter(
                empresa__cnpj=self.cnpj,
                mes_ref__gte=periodo_inicio,
                mes_ref__lte=periodo_fim
            ).aggregate(total=Sum('valor_iss'))['total'] or Decimal('0.00')
            
            arrecadacao_atual += iss_atual
            
            if incentivo.baseline_iss_12m:
                meses = (periodo_fim.year - periodo_inicio.year) * 12 + (periodo_fim.month - periodo_inicio.month) + 1
                baseline_total += (incentivo.baseline_iss_12m / 12) * meses
        
        if 'IPTU' in incentivo.tipo_incentivo or incentivo.tipo_incentivo in ['MISTO', 'TERRENO_GRATUITO']:
            iptu_atual = ArrecadacaoIPTU.objects.filter(
                empresa__cnpj=self.cnpj,
                ano_ref__gte=periodo_inicio.year,
                ano_ref__lte=periodo_fim.year
            ).aggregate(
                total_iptu=Sum('valor_iptu'),
                total_taxas=Sum('valor_taxas')
            )
            
            iptu_total = (iptu_atual['total_iptu'] or Decimal('0.00')) + (iptu_atual['total_taxas'] or Decimal('0.00'))
            arrecadacao_atual += iptu_total
            
            if incentivo.baseline_iptu_12m:
                anos = periodo_fim.year - periodo_inicio.year + 1
                baseline_total += incentivo.baseline_iptu_12m * anos
        
        return arrecadacao_atual - baseline_total
    
    def calcular_impacto_completo(self, periodo_inicio=None, periodo_fim=None):
        """Calcula todos os indicadores de impacto fiscal"""
        incentivo = Incentivo.objects.filter(empresa__cnpj=self.cnpj, status='ATIVO').first()
        
        if not incentivo:
            return None
        
        if not periodo_inicio:
            periodo_inicio = incentivo.data_inicio
        if not periodo_fim:
            periodo_fim = datetime.now().date()
        
        custo_fiscal = self.calcular_custo_fiscal(incentivo, periodo_inicio, periodo_fim)
        arrecadacao_incremental = self.calcular_arrecadacao_incremental(incentivo, periodo_inicio, periodo_fim)
        impacto_liquido = arrecadacao_incremental - custo_fiscal
        bc_ratio = arrecadacao_incremental / custo_fiscal if custo_fiscal > 0 else Decimal('0.00')
        
        if arrecadacao_incremental > 0:
            meses_periodo = (periodo_fim.year - periodo_inicio.year) * 12 + (periodo_fim.month - periodo_inicio.month) + 1
            arrecadacao_mensal = arrecadacao_incremental / meses_periodo
            payback_meses = int(custo_fiscal / arrecadacao_mensal) if arrecadacao_mensal > 0 else None
        else:
            payback_meses = None
        
        calculo, created = CalculoImpacto.objects.update_or_create(
            empresa=incentivo.empresa,
            periodo_inicio=periodo_inicio,
            periodo_fim=periodo_fim,
            defaults={
                'custo_fiscal': custo_fiscal,
                'arrecadacao_incremental': arrecadacao_incremental,
                'impacto_liquido': impacto_liquido,
                'bc_ratio': bc_ratio,
                'payback_meses': payback_meses
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
            'periodo_fim': periodo_fim
        }
