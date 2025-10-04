from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum, Avg
from django.http import HttpResponse
from datetime import datetime
import csv
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
from .services import CSVUploadService, AlertaService
from .utils import criar_auditoria

logger = logging.getLogger(__name__)


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['cnae', 'bairro', 'porte']
    search_fields = ['cnpj', 'razao_social', 'nome_fantasia']
    ordering_fields = ['razao_social']
    lookup_field = 'cnpj'
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'], url_path='upload-csv')
    def upload_csv(self, request):
        """Upload de CSV de empresas"""
        if 'file' not in request.FILES:
            return Response(
                {'error': 'Nenhum arquivo enviado'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            result = CSVUploadService.processar_empresas_csv(request.FILES['file'])
            criar_auditoria(
                request.user, 'UPLOAD', 
                detalhes='Upload CSV empresas', 
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return Response(result, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
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
        
        criar_auditoria(
            request.user, 'CONSULTA', cnpj=cnpj,
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
        
        criar_auditoria(
            request.user, 'EXPORTACAO',
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
            return Response(
                {'error': 'Nenhum arquivo enviado'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            result = CSVUploadService.processar_incentivos_csv(request.FILES['file'])
            return Response(result, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


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
            return Response(
                {'error': 'Nenhum arquivo enviado'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            result = CSVUploadService.processar_iss_csv(request.FILES['file'])
            return Response(result, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class ArrecadacaoIPTUViewSet(viewsets.ModelViewSet):
    queryset = ArrecadacaoIPTU.objects.all()
    serializer_class = ArrecadacaoIPTUSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'], url_path='upload-csv')
    def upload_csv(self, request):
        """Upload de CSV de arrecadação IPTU"""
        if 'file' not in request.FILES:
            return Response(
                {'error': 'Nenhum arquivo enviado'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            result = CSVUploadService.processar_iptu_csv(request.FILES['file'])
            return Response(result, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipo_alerta', 'severidade', 'status']
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'], url_path='gerar-alertas')
    def gerar_alertas(self, request):
        """Gera alertas automáticos baseados em regras"""
        result = AlertaService.gerar_todos_alertas()
        return Response(result)
    
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


# ViewSets adicionais para outros models
class ContrapartidaViewSet(viewsets.ModelViewSet):
    queryset = Contrapartida.objects.all()
    serializer_class = ContrapartidaSerializer
    permission_classes = [AllowAny]


class AuditoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Auditoria.objects.all()
    serializer_class = AuditoriaSerializer
    permission_classes = [AllowAny]
