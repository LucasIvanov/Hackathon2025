from django.core.management.base import BaseCommand
from api.models import UsuarioSistema

class Command(BaseCommand):
    help = 'Criar usuários de exemplo para o sistema'
    
    def handle(self, *args, **options):
        usuarios = [
            {
                'username': 'admin',
                'senha': 'admin123',
                'email': 'admin@semdec.cascavel.pr.gov.br',
                'nome_completo': 'Administrador do Sistema',
                'cargo': 'Coordenador',
                'departamento': 'SEMDEC'
            },
            {
                'username': 'analista1',
                'senha': 'senha123',
                'email': 'analista1@semdec.cascavel.pr.gov.br',
                'nome_completo': 'Maria Silva Santos',
                'cargo': 'Analista Fiscal',
                'departamento': 'SEMDEC - Tributação'
            },
            {
                'username': 'gestor',
                'senha': 'gestor123',
                'email': 'gestor@semdec.cascavel.pr.gov.br',
                'nome_completo': 'João Pedro Oliveira',
                'cargo': 'Gerente de Incentivos',
                'departamento': 'SEMDEC - Desenvolvimento'
            }
        ]
        
        created_count = 0
        
        for dados_usuario in usuarios:
            usuario, created = UsuarioSistema.objects.get_or_create(
                username=dados_usuario['username'],
                defaults=dados_usuario
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Usuário criado: {usuario.username} - {usuario.nome_completo}')
                )
            else:
                # Atualizar senha caso o usuário já exista
                usuario.senha = dados_usuario['senha']
                usuario.save()
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Usuário atualizado: {usuario.username}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Processo concluído! {created_count} usuários criados.')
        )
        
        self.stdout.write('\n🔐 Credenciais de acesso:')
        for dados_usuario in usuarios:
            self.stdout.write(f'   👤 {dados_usuario["username"]} / {dados_usuario["senha"]}')
