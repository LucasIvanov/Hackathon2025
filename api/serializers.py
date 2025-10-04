from rest_framework import serializers
from .models import (
    Empresa, Incentivo, ArrecadacaoISS, ArrecadacaoIPTU,
    Contrapartida, Alerta, CalculoImpacto, Auditoria
)


class EmpresaSerializer(serializers.ModelSerializer):
    total_incentivos = serializers.SerializerMethodField()
    
    class Meta:
        model = Empresa
        fields = '__all__'
        
    def get_total_incentivos(self, obj):
        return obj.incentivos.filter(status='ATIVO').count()


class IncentivoSerializer(serializers.ModelSerializer):
    empresa_razao_social = serializers.CharField(source='empresa.razao_social', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_incentivo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Incentivo
        fields = '__all__'


class ArrecadacaoISSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArrecadacaoISS
        fields = '__all__'


class ArrecadacaoIPTUSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArrecadacaoIPTU
        fields = '__all__'


class ContrapartidaSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Contrapartida
        fields = '__all__'


class AlertaSerializer(serializers.ModelSerializer):
    empresa_razao_social = serializers.CharField(source='empresa.razao_social', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_alerta_display', read_only=True)
    severidade_display = serializers.CharField(source='get_severidade_display', read_only=True)
    
    class Meta:
        model = Alerta
        fields = '__all__'


class CalculoImpactoSerializer(serializers.ModelSerializer):
    empresa_razao_social = serializers.CharField(source='empresa.razao_social', read_only=True)
    
    class Meta:
        model = CalculoImpacto
        fields = '__all__'


class AuditoriaSerializer(serializers.ModelSerializer):
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = Auditoria
        fields = '__all__'


class UploadCSVSerializer(serializers.Serializer):
    file = serializers.FileField()
    
    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Apenas arquivos CSV são permitidos")
        return value
