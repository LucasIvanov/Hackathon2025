# Sistema de Incentivos Fiscais - Hackathon SEMDEC 2025

## Descrição
Protótipo para o **Problema 5** do Hackathon FUNDETEC: **Plataforma de Acompanhamento de Incentivos - Retorno Fiscal por CNPJ**.

Sistema desenvolvido em Django REST Framework para controle e análise de incentivos fiscais municipais.

## Funcionalidades

### ✅ Implementadas
- 📊 **Dashboard executivo** com indicadores-chave
- 📈 **Cálculos automáticos**: Custo Fiscal (CF), Adicionalidade (AI), B/C Ratio, Payback
- 📁 **Upload de CSVs**: empresas, incentivos, arrecadação ISS e IPTU
- 🚨 **Sistema de alertas** automáticos
- 📋 **Relatórios executivos** com exportação
- 🔍 **Filtros** por CNAE, bairro, tipo de incentivo

### 📊 Indicadores Calculados
- **Custo Fiscal (CF)**: Renúncia fiscal total
- **Arrecadação Incremental (AI)**: Receita adicional gerada
- **Impacto Líquido**: AI - CF
- **B/C Ratio**: Relação Benefício/Custo
- **Payback**: Tempo de retorno do investimento
- **Ranking** por custo-benefício

## Como Executar

### 1. Clone o repositório
```bash
git clone https://github.com/LucasIvanov/Hackathon2025.git
cd Hackathon2025
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Execute as migrações
```bash
python manage.py migrate
```

### 4. Inicie o servidor
```bash
python manage.py runserver
```

### 5. Acesse a API
- **Base URL**: http://127.0.0.1:8000/api/
- **Admin**: http://127.0.0.1:8000/admin/

## Endpoints Principais

### 📊 Dashboard
- `GET /api/dashboard/resumo/` - Resumo executivo

### 🏢 Empresas
- `GET /api/empresas/` - Listar empresas
- `POST /api/empresas/upload-csv/` - Upload CSV de empresas
- `GET /api/empresas/{cnpj}/detalhe-completo/` - Detalhamento completo
- `GET /api/empresas/exportar-csv/` - Exportar relatório CSV

### 💰 Incentivos
- `GET /api/incentivos/` - Listar incentivos
- `POST /api/incentivos/upload-csv/` - Upload CSV de incentivos

### 📈 Arrecadação
- `POST /api/arrecadacao-iss/upload-csv/` - Upload ISS
- `POST /api/arrecadacao-iptu/upload-csv/` - Upload IPTU

### 🚨 Alertas
- `GET /api/alertas/` - Listar alertas ativos
- `POST /api/alertas/gerar-alertas/` - Gerar alertas automáticos

### 📊 Cálculos
- `GET /api/calculos/` - Listar cálculos de impacto
- `POST /api/calculos/calcular-todos/` - Calcular para todas empresas
- `GET /api/calculos/ranking/` - Ranking por B/C

## Formato dos CSVs

### Empresas (empresas.csv)
```csv
cnpj,razao_social,bairro
12345678000123,"Empresa Exemplo Ltda","Centro"
```

### Incentivos (incentivos.csv)
```csv
cnpj,instrumento_legal,tipo_incentivo,percentual_desconto,data_inicio,contrapartidas
12345678000123,"Lei 123/2023","ISENCAO_ISS",50.0,2023-01-01,"Gerar 10 empregos"
```

### Arrecadação ISS (arrecadacao_iss.csv)
```csv
cnpj,mes_ref,valor_iss
12345678000123,2023-01-01,5000.00
```

### Arrecadação IPTU (arrecadacao_iptu_taxas.csv)
```csv
cnpj,ano_ref,valor_iptu,valor_taxas
12345678000123,2023,15000.00,2000.00
```

## Tecnologias Utilizadas

- **Backend**: Django 5.2 + Django REST Framework
- **Banco**: SQLite (desenvolvimento)
- **Processamento**: Pandas para análise de dados
- **API**: REST com filtros e paginação

## Estrutura do Projeto

```
Hackathon2025/
├── manage.py
├── incentivos_fiscais/     # Configurações Django
├── api/                    # App principal
│   ├── models.py          # Modelos de dados
│   ├── views.py           # APIs e lógica
│   ├── serializers.py     # Serialização REST
│   ├── calculadora.py     # Cálculos fiscais
│   └── urls.py           # Rotas da API
├── db.sqlite3             # Banco de dados
└── requirements.txt       # Dependências
```

## Desenvolvido para
**Hackathon FUNDETEC 2025 - Problema 5**  
**Secretaria Municipal de Desenvolvimento Econômico (SEMDEC)**

---
*Protótipo funcional para demonstração e validação de conceitos*