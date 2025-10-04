from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
import logging

from .models import UsuarioSistema, Auditoria

logger = logging.getLogger(__name__)

class AuthViewSet(viewsets.ViewSet):
    """ViewSet para autenticação - CORRIGIDO"""
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login do usuário"""
        try:
            username = request.data.get('username')
            senha = request.data.get('senha')
            
            print(f"🔐 Login attempt: {username}")
            
            if not username or not senha:
                return Response({
                    'error': 'Username e senha são obrigatórios'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Buscar usuário
            usuario = UsuarioSistema.objects.get(
                username=username,
                senha=senha,
                ativo=True
            )
            
            print(f"✅ Usuário autenticado: {usuario.nome_completo}")
            
            # Atualizar último login
            usuario.ultimo_login = timezone.now()
            usuario.save()
            
            # Token simples para protótipo
            token = f'token_simples_{usuario.id}_{int(timezone.now().timestamp())}'
            
            response_data = {
                'success': True,
                'message': 'Login realizado com sucesso',
                'usuario': {
                    'id': usuario.id,
                    'username': usuario.username,
                    'nome_completo': usuario.nome_completo,
                    'email': usuario.email,
                    'cargo': usuario.cargo,
                    'departamento': usuario.departamento
                },
                'token': token
            }
            
            # Log de auditoria simplificado
            try:
                Auditoria.objects.create(
                    acao='LOGIN',
                    cnpj='',
                    detalhes=f'Login realizado por {usuario.nome_completo}',
                    usuario=usuario.username,
                    ip_address=request.META.get('REMOTE_ADDR', '127.0.0.1')
                )
            except Exception as audit_error:
                print(f"⚠️ Erro na auditoria: {audit_error}")
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except UsuarioSistema.DoesNotExist:
            print(f"❌ Usuário não encontrado: {username}")
            return Response({
                'error': 'Usuário ou senha inválidos'
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(f"❌ Erro no login: {str(e)}")
            return Response({
                'error': f'Erro interno: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def verificar_token(self, request):
        """Verificar se token é válido - CORRIGIDO"""
        try:
            # Tentar pegar token de várias formas
            auth_header = request.headers.get('Authorization', '')
            token = auth_header.replace('Bearer ', '') if auth_header else ''
            
            print(f"🔍 Token recebido: '{token[:50]}...' (truncated)")
            print(f"🔍 Auth header: '{auth_header}'")
            
            # Para protótipo, aceitar qualquer token que comece com token_simples_
            if token and token.startswith('token_simples_'):
                print("✅ Token válido")
                return Response({
                    'valid': True,
                    'message': 'Token válido'
                }, status=status.HTTP_200_OK)
            else:
                print(f"❌ Token inválido ou ausente: '{token}'")
                return Response({
                    'valid': False,
                    'message': 'Token inválido ou ausente'
                }, status=status.HTTP_401_UNAUTHORIZED)
                
        except Exception as e:
            print(f"❌ Erro na verificação: {str(e)}")
            return Response({
                'valid': False,
                'message': f'Erro na verificação: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Logout do usuário"""
        return Response({
            'success': True,
            'message': 'Logout realizado com sucesso'
        })
