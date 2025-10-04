from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum, Avg
from datetime import datetime, timedelta
import pandas as pd
import logging

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
    
    @action(detail=True, methods=['get'])
    def detalhe_completo(self, request, cnpj=None):
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
    
    @action(detail=False, methods=['post'])
    def upload_csv(self, request):
        serializer = UploadCSVSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            df = pd.read_csv(request.FILES['file'])
            count = 0
            
            for _, row in df.iterrows():
                Empresa.objects.update_or_create(
                    cnpj=row['cnpj'],
                    defaults={
                        'razao_social': row['razao_social'],
                        'nome_fantasia': row.get('nome_fantasia', ''),
                        'cnae': row['cnae'],
                        'cnae_descricao': row['cnae_descricao'],
                        'endereco': row['endereco'],
                        'bairro': row['bairro'],
                        'cidade': row.get('cidade', 'Cascavel'),
                        'uf': row.get('uf', 'PR'),
                        'data_abertura': row.get('data_abertura'),
                        'porte': row['porte']
                    }
                )
                count += 1
            
            return Response({'message': f'{count} empresas processadas', 'total': count}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class IncentivoViewSet(viewsets.ModelViewSet):
    queryset = Incentivo.objects.all()
    serializer_class = IncentivoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['tipo_incentivo', 'status']
    search_fields = ['empresa__cnpj', 'empresa__razao_social']
    
    @action(detail=False, methods=['post'])
    def upload_csv(self, request):
        serializer = UploadCSVSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            df = pd.read_csv(request.FILES['file'])
            count = 0
            
            for _, row in df.iterrows():
                empresa = Empresa.objects.get(cnpj=row['cnpj'])
                Incentivo.objects.create(
                    empresa=empresa,
                    instrumento_legal=row['instrumento_legal'],
                    tipo_incentivo=row['tipo_incentivo'],
                    percentual_desconto=row.get('percentual_desconto'),
                    valor_fixo_desconto=row.get('valor_fixo_desconto'),
                    data_inicio=row['data_inicio'],
                    data_fim=row.get('data_fim'),
                    contrapartidas=row.get('contrapartidas', ''),
                    status=row.get('status', 'ATIVO'),
                    baseline_iss_12m=row.get('baseline_iss_12m'),
                    baseline_iptu_12m=row.get('baseline_iptu_12m')
                )
                count += 1
            
            return Response({'message': f'{count} incentivos criados', 'total': count}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ArrecadacaoISSViewSet(viewsets.ModelViewSet):
    queryset = ArrecadacaoISS.objects.all()
    serializer_class = ArrecadacaoISSSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['empresa__cnpj', 'mes_ref']
    
    @action(detail=False, methods=['post'])
    def upload_csv(self, request):
        serializer = UploadCSVSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            df = pd.read_csv(request.FILES['file'])
            count = 0
            
            for _, row in df.iterrows():
                empresa = Empresa.objects.get(cnpj=row['cnpj'])
                ArrecadacaoISS.objects.update_or_create(
                    empresa=empresa,
                    mes_ref=row['mes_ref'],
                    defaults={
                        'valor_iss': row['valor_iss'],
                        'valor_base_calculo': row.get('valor_base_calculo'),
                        'aliquota': row.get('aliquota'),
                        'numero_nfse': row.get('numero_nfse', 0)
                    }
                )
                count += 1
            
            return Response({'message': f'{count} registros processados', 'total': count}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ArrecadacaoIPTUViewSet(viewsets.ModelViewSet):
    queryset = ArrecadacaoIPTU.objects.all()
    serializer_class = ArrecadacaoIPTUSerializer
    
    @action(detail=False, methods=['post'])
    def upload_csv(self, request):
        serializer = UploadCSVSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            df = pd.read_csv(request.FILES['file'])
            count = 0
            
            for _, row in df.iterrows():
                empresa = Empresa.objects.get(cnpj=row['cnpj'])
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
            
            return Response({'message': f'{count} registros processados', 'total': count}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipo_alerta', 'severidade', 'status']
    
    @action(detail=False, methods=['post'])
    def gerar_alertas(self, request):
        alertas_gerados = []
        
        # Alerta: B/C < 1
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
                            'descricao': f'B/C abaixo de 1: {calculo["bc_ratio"]:.4f}',
                            'severidade': 'ALTA'
                        }
                    )
                    if created:
                        alertas_gerados.append({'cnpj': empresa.cnpj, 'tipo': 'BC_BAIXO'})
            except:
                pass
        
        return Response({'message': f'{len(alertas_gerados)} alertas gerados', 'alertas': alertas_gerados})
    
    @action(detail=True, methods=['post'])
    def resolver(self, request, pk=None):
        alerta = self.get_object()
        alerta.status = 'RESOLVIDO'
        alerta.resolvido_em = datetime.now()
        alerta.resolvido_por = request.user
        alerta.save()
        return Response({'message': 'Alerta resolvido'})


class CalculoImpactoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CalculoImpacto.objects.all()
    serializer_class = CalculoImpactoSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['empresa__cnpj']
    ordering_fields = ['bc_ratio', 'impacto_liquido']
    
    @action(detail=False, methods=['post'])
    def calcular_todos(self, request):
        empresas = Empresa.objects.filter(incentivos__status='ATIVO').distinct()
        count = 0
        
        for empresa in empresas:
            try:
                calculadora = CalculadoraImpactoFiscal(empresa.cnpj)
                calculadora.calcular_impacto_completo()
                count += 1
            except:
                pass
        
        return Response({'message': f'Calculado para {count} empresas', 'total': count})
    
    @action(detail=False, methods=['get'])
    def ranking(self, request):
        tipo = request.query_params.get('tipo', 'melhores')
        limite = int(request.query_params.get('limite', 10))
        
        ordem = '-bc_ratio' if tipo == 'melhores' else 'bc_ratio'
        calculos = CalculoImpacto.objects.order_by(ordem)[:limite]
        
        return Response(CalculoImpactoSerializer(calculos, many=True).data)


class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def resumo(self, request):
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
            'custo_fiscal_total': agregados['custo_fiscal_total'] or 0,
            'arrecadacao_incremental_total': agregados['arrecadacao_incremental_total'] or 0,
            'impacto_liquido_total': agregados['impacto_liquido_total'] or 0,
            'bc_medio': agregados['bc_medio'] or 0,
            'total_alertas_ativos': total_alertas
        })
