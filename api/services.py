"""
Serviços para processamento de arquivos CSV
"""
import pandas as pd
import logging
from datetime import datetime
from .models import Empresa, Incentivo, ArrecadacaoISS, ArrecadacaoIPTU
from .utils import processar_linha_empresa, formatar_response_upload

logger = logging.getLogger(__name__)

class CSVUploadService:
    """
    Serviço para processamento de uploads CSV
    """
    
    @staticmethod
    def processar_empresas_csv(file):
        """
        Processa arquivo CSV de empresas
        """
        try:
            df = pd.read_csv(file)
            count = 0
            errors = []
            
            for idx, row in df.iterrows():
                try:
                    dados_empresa = processar_linha_empresa(row)
                    
                    # Adicionar data_abertura se existir
                    if 'data_abertura' in row and pd.notna(row['data_abertura']):
                        dados_empresa['data_abertura'] = row['data_abertura']
                    
                    Empresa.objects.update_or_create(
                        cnpj=dados_empresa['cnpj'],
                        defaults=dados_empresa
                    )
                    count += 1
                except Exception as e:
                    errors.append(f"Linha {idx + 2}: {str(e)}")
                    logger.error(f"Erro na linha {idx + 2}: {str(e)}")
            
            return formatar_response_upload(count, errors, 'empresas')
            
        except Exception as e:
            logger.error(f"Erro no upload de empresas: {str(e)}")
            raise Exception(f'Erro ao processar arquivo: {str(e)}')
    
    @staticmethod
    def processar_incentivos_csv(file):
        """
        Processa arquivo CSV de incentivos
        """
        try:
            df = pd.read_csv(file)
            count = 0
            errors = []
            
            for idx, row in df.iterrows():
                try:
                    empresa = Empresa.objects.get(cnpj=str(row['cnpj']).strip())
                    
                    Incentivo.objects.create(
                        empresa=empresa,
                        instrumento_legal=str(row['instrumento_legal']),
                        tipo_incentivo=str(row['tipo_incentivo']),
                        percentual_desconto=row.get('percentual_desconto') if pd.notna(row.get('percentual_desconto')) else None,
                        valor_fixo_desconto=row.get('valor_fixo_desconto') if pd.notna(row.get('valor_fixo_desconto')) else None,
                        data_inicio=row['data_inicio'],
                        data_fim=row.get('data_fim') if pd.notna(row.get('data_fim')) else None,
                        contrapartidas=str(row.get('contrapartidas', '')),
                        status=str(row.get('status', 'ATIVO')),
                        baseline_iss_12m=row.get('baseline_iss_12m') if pd.notna(row.get('baseline_iss_12m')) else None,
                        baseline_iptu_12m=row.get('baseline_iptu_12m') if pd.notna(row.get('baseline_iptu_12m')) else None
                    )
                    count += 1
                except Empresa.DoesNotExist:
                    errors.append(f"Linha {idx + 2}: Empresa CNPJ {row['cnpj']} não encontrada")
                except Exception as e:
                    errors.append(f"Linha {idx + 2}: {str(e)}")
            
            return formatar_response_upload(count, errors, 'incentivos')
            
        except Exception as e:
            logger.error(f"Erro no upload de incentivos: {str(e)}")
            raise Exception(f'Erro ao processar arquivo: {str(e)}')
    
    @staticmethod
    def processar_iss_csv(file):
        """
        Processa arquivo CSV de arrecadação ISS
        """
        try:
            df = pd.read_csv(file)
            count = 0
            errors = []
            
            for idx, row in df.iterrows():
                try:
                    empresa = Empresa.objects.get(cnpj=str(row['cnpj']).strip())
                    
                    ArrecadacaoISS.objects.update_or_create(
                        empresa=empresa,
                        mes_ref=row['mes_ref'],
                        defaults={
                            'valor_iss': row['valor_iss'],
                            'valor_base_calculo': row.get('valor_base_calculo') if pd.notna(row.get('valor_base_calculo')) else None,
                            'aliquota': row.get('aliquota') if pd.notna(row.get('aliquota')) else None,
                            'numero_nfse': row.get('numero_nfse', 0)
                        }
                    )
                    count += 1
                except Empresa.DoesNotExist:
                    errors.append(f"Linha {idx + 2}: Empresa CNPJ {row['cnpj']} não encontrada")
                except Exception as e:
                    errors.append(f"Linha {idx + 2}: {str(e)}")
            
            return formatar_response_upload(count, errors, 'registros de ISS')
            
        except Exception as e:
            logger.error(f"Erro no upload de ISS: {str(e)}")
            raise Exception(f'Erro ao processar arquivo: {str(e)}')
    
    @staticmethod
    def processar_iptu_csv(file):
        """
        Processa arquivo CSV de arrecadação IPTU
        """
        try:
            df = pd.read_csv(file)
            count = 0
            errors = []
            
            for idx, row in df.iterrows():
                try:
                    empresa = Empresa.objects.get(cnpj=str(row['cnpj']).strip())
                    
                    ArrecadacaoIPTU.objects.update_or_create(
                        empresa=empresa,
                        ano_ref=row['ano_ref'],
                        defaults={
                            'valor_iptu': row['valor_iptu'],
                            'valor_taxas': row['valor_taxas'],
                            'valor_alvara': row.get('valor_alvara', 0)
                        }
                    )
                    count += 1
                except Empresa.DoesNotExist:
                    errors.append(f"Linha {idx + 2}: Empresa CNPJ {row['cnpj']} não encontrada")
                except Exception as e:
                    errors.append(f"Linha {idx + 2}: {str(e)}")
            
            return formatar_response_upload(count, errors, 'registros de IPTU')
            
        except Exception as e:
            logger.error(f"Erro no upload de IPTU: {str(e)}")
            raise Exception(f'Erro ao processar arquivo: {str(e)}')

class AlertaService:
    """
    Serviço para geração de alertas
    """
    
    @staticmethod
    def gerar_todos_alertas():
        """
        Gera todos os tipos de alertas automáticos
        """
        from .utils import gerar_alerta_bc_baixo, gerar_alerta_sem_recolhimento, gerar_alerta_contrapartida_vencendo
        from .models import Contrapartida
        from datetime import datetime, timedelta
        
        alertas_gerados = []
        
        # Alerta 1: B/C < 1
        empresas = Empresa.objects.filter(incentivos__status='ATIVO').distinct()
        for empresa in empresas:
            if gerar_alerta_bc_baixo(empresa):
                alertas_gerados.append({'cnpj': empresa.cnpj, 'tipo': 'BC_BAIXO'})
        
        # Alerta 2: Sem recolhimento por 3 meses
        empresas_ativas = Empresa.objects.filter(incentivos__status='ATIVO').distinct()
        for empresa in empresas_ativas:
            if gerar_alerta_sem_recolhimento(empresa):
                alertas_gerados.append({'cnpj': empresa.cnpj, 'tipo': 'SEM_RECOLHIMENTO'})
        
        # Alerta 3: Contrapartidas vencendo em 30 dias
        prazo_30_dias = datetime.now().date() + timedelta(days=30)
        contrapartidas_vencendo = Contrapartida.objects.filter(
            status='PENDENTE',
            data_vencimento__lte=prazo_30_dias,
            data_vencimento__gte=datetime.now().date()
        )
        
        for contrapartida in contrapartidas_vencendo:
            if gerar_alerta_contrapartida_vencendo(contrapartida):
                alertas_gerados.append({
                    'cnpj': contrapartida.incentivo.empresa.cnpj, 
                    'tipo': 'CONTRAPARTIDA_VENCENDO'
                })
        
        return {
            'message': f'{len(alertas_gerados)} alertas gerados',
            'alertas': alertas_gerados
        }
