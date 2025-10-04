from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone

from .models import UsuarioSistema, Auditoria

class AuthViewSet(viewsets.ViewSet):
    """ViewSet simplificado para autenticação"""
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login do usuário"""
        try:
            username = request.data.get('username')
            senha = request.data.get('senha')
            
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
            
            # Atualizar último login
            usuario.ultimo_login = timezone.now()
            usuario.save()
            
            # Token simples
            token = f'valid_token_{usuario.id}_{int(timezone.now().timestamp())}'
            
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
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except UsuarioSistema.DoesNotExist:
            return Response({
                'error': 'Usuário ou senha inválidos'
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'error': f'Erro interno: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def verificar_token(self, request):
        """Verificar token - SIMPLIFICADO"""
        # Para protótipo, sempre retornar válido se há algum token
        auth_header = request.headers.get('Authorization', '')
        
        print(f"🔍 Headers: {dict(request.headers)}")
        print(f"🔍 Auth header: '{auth_header}'")
        
        if auth_header and ('token' in auth_header.lower() or auth_header.startswith('Bearer')):
            return Response({
                'valid': True,
                'message': 'Token válido'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'valid': False,
            'message': 'Token ausente'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Logout"""
        return Response({
            'success': True,
            'message': 'Logout realizado'
        })
