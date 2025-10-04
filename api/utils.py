"""
Funções auxiliares para o projeto
"""
import random
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum
from .models import Empresa, ArrecadacaoISS, Contrapartida, Alerta

logger = logging.getLogger(__name__)

# Mapeamento de CNAEs
CNAES_DESCRICAO = {
    '8610': 'Atividades de atendimento hospitalar',
    '4722': 'Comércio varejista de carnes e pescados',
    '4731': 'Comércio varejista de combustíveis',
    '4120': 'Construção de edifícios',
    '1091': 'Fabricação de produtos de panificação',
    '1610': 'Desdobramento de madeira',
    '4635': 'Comércio atacadista de café',
    '4930': 'Transporte rodoviário de carga',
    '4724': 'Comércio varejista de hortifrutigranjeiros',
    '6201': 'Desenvolvimento de programas de computador',
    '9313': 'Atividades de condicionamento físico',
    '1011': 'Frigorífico - abate de bovinos',
    '8541': 'Educação profissional técnica',
    '4530': 'Comércio de peças e acessórios',
    '2512': 'Fabricação de esquadrias de metal',
    '5510': 'Hotéis e similares',
    '4520': 'Manutenção e reparação mecânica'
}

def determinar_porte_empresa(razao_social):
    """
    Determina o porte da empresa baseado na razão social
    """
    if 'SA' in razao_social or 'S.A.' in razao_social:
        return 'GRANDE'
    elif 'Ltda' in razao_social:
        return random.choice(['ME', 'EPP'])
    else:
        return 'ME'

def processar_linha_empresa(row):
    """
    Processa uma linha do CSV de empresas
    """
    cnae = str(row['cnae'])
    razao_social = str(row['razao_social'])
    porte = determinar_porte_empresa(razao_social)
    
    return {
        'cnpj': str(row['cnpj']).strip(),
        'razao_social': razao_social,
        'nome_fantasia': razao_social.replace(' Ltda', '').replace(' SA', ''),
        'cnae': cnae,
        'cnae_descricao': CNAES_DESCRICAO.get(cnae, 'Outras atividades'),
        'endereco': f'Rua Comercial, {row["bairro"]}',
        'bairro': str(row['bairro']),
        'cidade': 'Cascavel',
        'uf': 'PR',
        'porte': porte
    }

def criar_auditoria(usuario, acao, cnpj=None, detalhes=None, ip_address=None):
    """
    Cria registro de auditoria
    """
    from .models import Auditoria
    
    Auditoria.objects.create(
        usuario=usuario if usuario and usuario.is_authenticated else None,
        acao=acao,
        cnpj=cnpj,
        detalhes=detalhes,
        ip_address=ip_address
    )

def gerar_alerta_bc_baixo(empresa):
    """
    Gera alerta para B/C baixo
    """
    from .calculadora import CalculadoraImpactoFiscal
    
    try:
        calculadora = CalculadoraImpactoFiscal(empresa.cnpj)
        calculo = calculadora.calcular_impacto_completo()
        
        if calculo and calculo['bc_ratio'] < 1:
            alerta, created = Alerta.objects.get_or_create(
                empresa=empresa,
                tipo_alerta='BC_BAIXO',
                status='ATIVO',
                defaults={
                    'descricao': f'Relação B/C abaixo de 1: {calculo["bc_ratio"]:.4f}',
                    'severidade': 'ALTA'
                }
            )
            return created
    except Exception as e:
        logger.error(f"Erro ao gerar alerta B/C para {empresa.cnpj}: {str(e)}")
    
    return False

def gerar_alerta_sem_recolhimento(empresa):
    """
    Gera alerta para empresa sem recolhimento
    """
    tres_meses_atras = datetime.now().date() - timedelta(days=90)
    
    tem_recolhimento = ArrecadacaoISS.objects.filter(
        empresa=empresa,
        mes_ref__gte=tres_meses_atras,
        valor_iss__gt=0
    ).exists()
    
    if not tem_recolhimento:
        alerta, created = Alerta.objects.get_or_create(
            empresa=empresa,
            tipo_alerta='SEM_RECOLHIMENTO',
            status='ATIVO',
            defaults={
                'descricao': 'Empresa sem recolhimento de ISS nos últimos 3 meses',
                'severidade': 'MEDIA'
            }
        )
        return created
    
    return False

def gerar_alerta_contrapartida_vencendo(contrapartida):
    """
    Gera alerta para contrapartida vencendo
    """
    alerta, created = Alerta.objects.get_or_create(
        empresa=contrapartida.incentivo.empresa,
        tipo_alerta='CONTRAPARTIDA_VENCENDO',
        status='ATIVO',
        defaults={
            'descricao': f'Contrapartida vencendo em {contrapartida.data_vencimento}: {contrapartida.descricao}',
            'severidade': 'ALTA'
        }
    )
    return created

def formatar_response_upload(count, errors=None, tipo='registros'):
    """
    Formata resposta padrão para uploads
    """
    response_data = {
        'message': f'{count} {tipo} processados com sucesso',
        'total': count
    }
    
    if errors and len(errors) <= 10:
        response_data['errors'] = errors
        
    return response_data
