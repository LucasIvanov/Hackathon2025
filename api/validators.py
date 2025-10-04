"""
Validadores customizados para o projeto
"""
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def validar_cnpj(cnpj):
    """
    Valida se o CNPJ é válido
    """
    # Remove caracteres não numéricos
    cnpj = re.sub(r'\D', '', cnpj)
    
    # Verifica se tem 14 dígitos
    if len(cnpj) != 14:
        raise ValidationError('CNPJ deve ter 14 dígitos')
    
    # Verifica se não são todos iguais
    if cnpj == cnpj[0] * 14:
        raise ValidationError('CNPJ inválido')
    
    # Cálculo do primeiro dígito verificador
    peso = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * peso[i] for i in range(12))
    resto = soma % 11
    dv1 = 0 if resto < 2 else 11 - resto
    
    if int(cnpj[12]) != dv1:
        raise ValidationError('CNPJ inválido')
    
    # Cálculo do segundo dígito verificador
    peso = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * peso[i] for i in range(13))
    resto = soma % 11
    dv2 = 0 if resto < 2 else 11 - resto
    
    if int(cnpj[13]) != dv2:
        raise ValidationError('CNPJ inválido')
    
    return cnpj

def validar_arquivo_csv(arquivo):
    """
    Valida se o arquivo enviado é um CSV válido
    """
    if not arquivo.name.endswith('.csv'):
        raise ValidationError('Apenas arquivos CSV são permitidos')
    
    if arquivo.size > 10 * 1024 * 1024:  # 10MB
        raise ValidationError('Arquivo muito grande. Máximo 10MB')
    
    return arquivo

def validar_percentual(valor):
    """
    Valida se o percentual está entre 0 e 100
    """
    if valor < 0 or valor > 100:
        raise ValidationError('Percentual deve estar entre 0 e 100')
    
    return valor

# Validadores de regex
cnpj_validator = RegexValidator(
    regex=r'^\d{14}$',
    message='CNPJ deve conter exatamente 14 dígitos',
    code='invalid_cnpj'
)

cnae_validator = RegexValidator(
    regex=r'^\d{4}$',
    message='CNAE deve conter exatamente 4 dígitos',
    code='invalid_cnae'
)
