from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum, Avg
from django.http import HttpResponse
from datetime import datetime, timedelta
import pandas as pd
import logging
import csv
import random

from .models import (
    Empresa, Incentivo, ArrecadacaoISS, ArrecadacaoIPTU,
    Contrapartida, Alerta, CalculoImpacto, Auditoria
)
from .serializers import (
    EmpresaSerializer, IncentivoSerializer,
    ArrecadacaoISSSerializer, ArrecadacaoIPTUSerializer,
    ContrapartidaSerializer, AlertaSerializer, CalculoImpactoSerializer,
    AuditoriaSerializer, UploadCSVSerializer
)
from .calculadora import CalculadoraImpactoFiscal

logger = logging.getLogger(__name__)


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['cnae', 'bairro', 'porte']
    search_fields = ['cnpj', 'razao_social', 'nome_fantasia']
    ordering_fields = ['razao_social']
    lookup_field = 'cnpj'
    permission_classes = [AllowAny]  # Permite acesso sem autenticação
    
    @action(detail=False, methods=['post'], url_path='upload-csv')
    def upload_csv(self, request):
        """Upload de CSV de empresas"""
        if 'file' not in request.FILES:
            return Response({'error': 'Nenhum arquivo enviado'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Mapeamento de CNAEs
        cnaes_desc = {
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
        
        try:
            df = pd.read_csv(request.FILES['file'])
            count = 0
            errors = []
            
            for idx, row in df.iterrows():
                try:
                    cnae = str(row['cnae'])
                    razao_social = str(row['razao_social'])
                    
                    # Determinar porte baseado na razão social
                    if 'SA' in razao_social or 'S.A.' in razao_social:
                        porte = 'GRANDE'
                    elif 'Ltda' in razao_social:
                        porte = random.choice(['ME', 'EPP'])
                    else:
                        porte = 'ME'
                    
                    Empresa.objects.update_or_create(
                        cnpj=str(row['cnpj']).strip(),
                        defaults={
                            'razao_social': razao_social,
                            'nome_fantasia': razao_social.replace(' Ltda', '').replace(' SA', ''),
                            'cnae': cnae,
                            'cnae_descricao': cnaes_desc.get(cnae, 'Outras atividades'),
                            'endereco': f'Rua Comercial, {row["bairro"]}',
                            'bairro': str(row['bairro']),
                            'cidade': 'Cascavel',
                            'uf': 'PR',
                            'data_abertura': row.get('data_abertura') if pd.notna(row.get('data_abertura')) else None,
                            'porte': porte
                        }
                    )
                    count += 1
                except Exception as e:
                    errors.append(f"Linha {idx + 2}: {str(e)}")
                    logger.error(f"Erro na linha {idx + 2}: {str(e)}")
            
            response_data = {
                'message': f'{count} empresas processadas com sucesso',
                'total': count
            }
            if errors and len(errors) <= 10:
                response_data['errors'] = errors
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Erro no upload: {str(e)}")
            return Response({
                'error': f'Erro ao processar arquivo: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], url_path='detalhe-completo')
    def detalhe_completo(self, request, cnpj=None):
        """Retorna detalhamento completo da empresa"""
        empresa = self.get_object()
        calculadora = CalculadoraImpactoFiscal(cnpj)
        calculo = calculadora.calcular_impacto_completo()
        
        data = {
            'empresa': EmpresaSerializer(empresa).data,
            'incentivos': IncentivoSerializer(empresa.incentivos.all(), many=True).data,
            'calculo_impacto': calculo,
            'alertas': AlertaSerializer(empresa.alertas.filter(status='ATIVO'), many=True).data,
            'historico_iss': ArrecadacaoISSSerializer(empresa.arrecadacao_iss.all()[:24], many=True).data,
        }
        
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            acao='CONSULTA',
            cnpj=cnpj,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return Response(data)
    
    @action(detail=False, methods=['get'], url_path='exportar-csv')
    def exportar_csv(self, request):
        """Exporta lista de empresas em CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="empresas.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['CNPJ', 'Razão Social', 'CNAE', 'Bairro', 'Porte'])
        
        empresas = self.get_queryset()
        for empresa in empresas:
            writer.writerow([
                empresa.cnpj,
                empresa.razao_social,
                empresa.cnae_descricao,
                empresa.bairro,
                empresa.porte
            ])
        
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            acao='EXPORTACAO',
            detalhes='Exportação CSV de empresas',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return response
    
    @action(detail=True, methods=['get'], url_path='exportar-relatorio-pdf')
    def exportar_relatorio_pdf(self, request, cnpj=None):
        """Gera relatório executivo em formato JSON (PDF em produção)"""
        empresa = self.get_object()
        calculadora = CalculadoraImpactoFiscal(cnpj)
        calculo = calculadora.calcular_impacto_completo()
        
        relatorio = {
            'empresa': EmpresaSerializer(empresa).data,
            'incentivos': IncentivoSerializer(empresa.incentivos.all(), many=True).data,
            'calculo_impacto': calculo,
            'gerado_em': datetime.now().isoformat()
        }
        
        return Response(relatorio)


class IncentivoViewSet(viewsets.ModelViewSet):
    queryset = Incentivo.objects.all()
    serializer_class = IncentivoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['tipo_incentivo', 'status']
    search_fields = ['empresa__cnpj', 'empresa__razao_social']
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'], url_path='upload-csv')
    def upload_csv(self, request):
        """Upload de CSV de incentivos"""
        if 'file' not in request.FILES:
            return Response({'error': 'Nenhum arquivo enviado'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            df = pd.read_csv(request.FILES['file'])
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
            
            response_data = {
                'message': f'{count} incentivos criados com sucesso',
                'total': count
            }
            if errors and len(errors) <= 10:
                response_data['errors'] = errors
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Erro no upload: {str(e)}")
            return Response({
                'error': f'Erro ao processar arquivo: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)


class ArrecadacaoISSViewSet(viewsets.ModelViewSet):
    queryset = ArrecadacaoISS.objects.all()
    serializer_class = ArrecadacaoISSSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['empresa__cnpj', 'mes_ref']
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'], url_path='upload-csv')
    def upload_csv(self, request):
        """Upload de CSV de arrecadação ISS"""
        if 'file' not in request.FILES:
            return Response({'error': 'Nenhum arquivo enviado'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            df = pd.read_csv(request.FILES['file'])
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
            
            response_data = {
                'message': f'{count} registros de ISS processados',
                'total': count
            }
            if errors and len(errors) <= 10:
                response_data['errors'] = errors
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Erro no upload: {str(e)}")
            return Response({
                'error': f'Erro ao processar arquivo: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)


class ArrecadacaoIPTUViewSet(viewsets.ModelViewSet):
    queryset = ArrecadacaoIPTU.objects.all()
    serializer_class = ArrecadacaoIPTUSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'], url_path='upload-csv')
    def upload_csv(self, request):
        """Upload de CSV de arrecadação IPTU"""
        if 'file' not in request.FILES:
            return Response({'error': 'Nenhum arquivo enviado'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            df = pd.read_csv(request.FILES['file'])
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
            
            response_data = {
                'message': f'{count} registros de IPTU processados',
                'total': count
            }
            if errors and len(errors) <= 10:
                response_data['errors'] = errors
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Erro no upload: {str(e)}")
            return Response({
                'error': f'Erro ao processar arquivo: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)


class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipo_alerta', 'severidade', 'status']
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'], url_path='gerar-alertas')
    def gerar_alertas(self, request):
        """Gera alertas automáticos baseados em regras"""
        alertas_gerados = []
        
        # Alerta 1: B/C < 1
        empresas = Empresa.objects.filter(incentivos__status='ATIVO').distinct()
        for empresa in empresas:
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
                    if created:
                        alertas_gerados.append({'cnpj': empresa.cnpj, 'tipo': 'BC_BAIXO'})
            except Exception as e:
                logger.error(f"Erro ao gerar alerta B/C para {empresa.cnpj}: {str(e)}")
        
        # Alerta 2: Sem recolhimento por 3 meses
        tres_meses_atras = datetime.now().date() - timedelta(days=90)
        empresas_ativas = Empresa.objects.filter(incentivos__status='ATIVO').distinct()
        
        for empresa in empresas_ativas:
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
                if created:
                    alertas_gerados.append({'cnpj': empresa.cnpj, 'tipo': 'SEM_RECOLHIMENTO'})
        
        # Alerta 3: Contrapartidas vencendo em 30 dias
        prazo_30_dias = datetime.now().date() + timedelta(days=30)
        contrapartidas_vencendo = Contrapartida.objects.filter(
            status='PENDENTE',
            data_vencimento__lte=prazo_30_dias,
            data_vencimento__gte=datetime.now().date()
        )
        
        for contrapartida in contrapartidas_vencendo:
            alerta, created = Alerta.objects.get_or_create(
                empresa=contrapartida.incentivo.empresa,
                tipo_alerta='CONTRAPARTIDA_VENCENDO',
                status='ATIVO',
                defaults={
                    'descricao': f'Contrapartida vencendo em {contrapartida.data_vencimento}: {contrapartida.descricao}',
                    'severidade': 'ALTA'
                }
            )
            if created:
                alertas_gerados.append({'cnpj': contrapartida.incentivo.empresa.cnpj, 'tipo': 'CONTRAPARTIDA_VENCENDO'})
        
        return Response({
            'message': f'{len(alertas_gerados)} alertas gerados',
            'alertas': alertas_gerados
        })
    
    @action(detail=True, methods=['post'])
    def resolver(self, request, pk=None):
        """Marca um alerta como resolvido"""
        alerta = self.get_object()
        alerta.status = 'RESOLVIDO'
        alerta.resolvido_em = datetime.now()
        alerta.resolvido_por = request.user if request.user.is_authenticated else None
        alerta.observacoes = request.data.get('observacoes', '')
        alerta.save()
        return Response({'message': 'Alerta resolvido com sucesso'})


class CalculoImpactoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CalculoImpacto.objects.all()
    serializer_class = CalculoImpactoSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['empresa__cnpj']
    ordering_fields = ['bc_ratio', 'impacto_liquido']
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'], url_path='calcular-todos')
    def calcular_todos(self, request):
        """Calcula impacto para todas as empresas com incentivo ativo"""
        empresas = Empresa.objects.filter(incentivos__status='ATIVO').distinct()
        count = 0
        errors = []
        
        for empresa in empresas:
            try:
                calculadora = CalculadoraImpactoFiscal(empresa.cnpj)
                calculadora.calcular_impacto_completo()
                count += 1
            except Exception as e:
                errors.append(f"Erro em {empresa.cnpj}: {str(e)}")
                logger.error(f"Erro ao calcular {empresa.cnpj}: {str(e)}")
        
        response_data = {
            'message': f'Calculado para {count} empresas',
            'total': count
        }
        if errors and len(errors) <= 10:
            response_data['errors'] = errors
        
        return Response(response_data)
    
    @action(detail=False, methods=['get'])
    def ranking(self, request):
        """Retorna ranking de empresas por B/C"""
        tipo = request.query_params.get('tipo', 'melhores')
        limite = int(request.query_params.get('limite', 10))
        
        ordem = '-bc_ratio' if tipo == 'melhores' else 'bc_ratio'
        calculos = CalculoImpacto.objects.order_by(ordem)[:limite]
        
        return Response(CalculoImpactoSerializer(calculos, many=True).data)


class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def resumo(self, request):
        """Retorna resumo executivo do dashboard"""
        total_incentivos = Incentivo.objects.filter(status='ATIVO').count()
        total_empresas = Empresa.objects.filter(incentivos__status='ATIVO').distinct().count()
        
        agregados = CalculoImpacto.objects.aggregate(
            custo_fiscal_total=Sum('custo_fiscal'),
            arrecadacao_incremental_total=Sum('arrecadacao_incremental'),
            impacto_liquido_total=Sum('impacto_liquido'),
            bc_medio=Avg('bc_ratio')
        )
        
        total_alertas = Alerta.objects.filter(status='ATIVO').count()
        
        return Response({
            'total_incentivos_ativos': total_incentivos,
            'total_empresas': total_empresas,
            'custo_fiscal_total': float(agregados['custo_fiscal_total'] or 0),
            'arrecadacao_incremental_total': float(agregados['arrecadacao_incremental_total'] or 0),
            'impacto_liquido_total': float(agregados['impacto_liquido_total'] or 0),
            'bc_medio': float(agregados['bc_medio'] or 0),
            'total_alertas_ativos': total_alertas
        })
