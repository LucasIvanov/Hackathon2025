import pandas as pd
import random
from datetime import datetime, timedelta

# Gerar CSV de empresas com todas as colunas necessárias
cnaes = {
    '8610': 'Atividades de atendimento hospitalar',
    '4722': 'Comércio varejista de carnes e pescados',
    '4731': 'Comércio varejista de combustíveis',
    '4120': 'Construção de edifícios',
    '1091': 'Fabricação de produtos de panificação',
    '1610': 'Desdobramento de madeira',
    '4635': 'Comércio atacadista de café em grão',
    '4930': 'Transporte rodoviário de carga',
    '4724': 'Comércio varejista de hortifrutigranjeiros',
    '6201': 'Desenvolvimento de programas de computador',
    '9313': 'Atividades de condicionamento físico',
    '1011': 'Frigorífico - abate de bovinos',
    '8541': 'Educação profissional de nível técnico',
    '4530': 'Comércio de peças e acessórios',
    '2512': 'Fabricação de esquadrias de metal',
    '5510': 'Hotéis e similares',
    '4520': 'Serviços de manutenção e reparação mecânica'
}

portes = ['MEI', 'ME', 'EPP', 'MEDIA', 'GRANDE']
bairros = ['Centro', 'Santa Cruz', 'Floresta', 'Cascavel Velho', 'Perímetro Urbano', 
           'Coqueiral', 'Brasmadeira', 'Lagoa', 'Pacaembu']

# Ler CSV existente
df_old = pd.read_csv('/home/vinicius/Documentos/qualquercoisa/Hackathon2025/api/media/empresas.csv')

# Criar novo DataFrame com todas as colunas
empresas_data = []

for _, row in df_old.iterrows():
    cnae = str(row['cnae'])
    empresas_data.append({
        'cnpj': row['cnpj'],
        'razao_social': row['razao_social'],
        'nome_fantasia': row['razao_social'].replace(' Ltda', '').replace(' SA', ''),
        'cnae': cnae,
        'cnae_descricao': cnaes.get(cnae, 'Outras atividades'),
        'endereco': f'Rua {random.choice(["Principal", "Central", "Comercial"])} {random.randint(100, 999)}',
        'bairro': row['bairro'],
        'cidade': 'Cascavel',
        'uf': 'PR',
        'data_abertura': row['data_abertura'],
        'porte': random.choice(portes)
    })

df_empresas = pd.DataFrame(empresas_data)
df_empresas.to_csv('empresas_completo.csv', index=False)

print(f"✅ Gerado empresas_completo.csv com {len(df_empresas)} registros")
print(f"Colunas: {', '.join(df_empresas.columns)}")
