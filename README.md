# 🍻 AB InBev Data Pipeline (Medallion Architecture)

## 🎯 Objetivo

Este projeto implementa um pipeline de dados em três camadas (Bronze → Silver → Gold) utilizando Python, pandas, PyArrow, S3 e Apache Airflow. Cada estágio do pipeline transforma os dados de forma incremental, culminando em agregações úteis para análise.

---

🌐 Fonte dos Dados
Este projeto utiliza dados reais disponibilizados por uma API pública:

https://www.openbrewerydb.org/

API: https://api.openbrewerydb.org/breweries

Os dados são extraídos no formato JSON e salvos na camada Bronze para posterior transformação e análise.

---

## ⚙️ Tecnologias

- Airflow
- AWS S3
- Python (pandas, boto3, pyarrow)
- Docker / Docker Compose

---

## 📐 Arquitetura e Design

- **Camada Bronze:** ingestão bruta dos JSONs.
- **Silver:** limpeza e divisão por estado.
- **Gold:** agregações por tipo e estado.

---

## ▶️ Execução Local

1. Crie `.env` com variáveis AWS:

## 🚀 Como Executar Localmente

### 1. Pré-requisitos

Python 3.12+

pip install -r requirements.txt com pacotes como:

- boto3
- requests
- pandas
- pyarrow

---

### 2. Configurar variáveis de ambiente

Crie um arquivo .env com as credenciais:

AWS_ACCESS_KEY_ID=SEU_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=SEU_SECRET
AWS_DEFAULT_REGION=us-east-2
S3_BUCKET=ab-inbev-data-pipeline

Carregue-as no terminal com:
set -a; source .env; set +a

---

## 📁 Estrutura de Pastas

.
├── scripts/
│   ├── bronze_ingest.py         # Lê arquivos JSON da camada Bronze
│   ├── silver_transform.py      # Limpa e transforma dados por estado
│   └── gold_transform.py        # Agrega dados por tipo/estado
├── dags/
│   ├── bronze_dag.py            # DAG do Airflow para Bronze
│   ├── silver_dag.py            # DAG do Airflow para Silver
│   └── gold_dag.py              # DAG do Airflow para Gold
├── tests/
│   ├── test_silver_transform.py # Teste da transformação Silver
│   └── test_gold_transform.py   # Teste da transformação Gold
├── .env                         # Variáveis de ambiente
└── README.md

---

## 🧠 Decisões de Design

- PyArrow: alta performance para serialização/deserialização .parquet

- Mock de boto3: evita dependência com AWS durante testes

- Arquitetura em camadas: garante rastreabilidade e escalabilidade

- Particionamento por estado: otimiza consultas e leitura de dados

- Testes automatizados: validam tanto a escrita quanto a estrutura dos dados

---

## ⚙️ Execução no Airflow

Cada camada possui uma DAG independente no Airflow:

bronze_dag.py: executa o ingest de arquivos JSON do S3

silver_dag.py: processa e particiona os dados por estado

gold_dag.py: executa agregações para análise

---

## 📬 Monitoramento e Alertas

Cada DAG pode conter lógica de alerta via e-mail para falhas:

default_args = {
    "email": ["voce@exemplo.com"],
    "email_on_failure": True,
    ...
}

---

## ☁️ Configuração da Nuvem (AWS)

Crie um bucket S3: ab-inbev-data-pipeline

Configure uma Role ou IAM User com permissões s3:PutObject, s3:GetObject, s3:ListBucket

Adicione arquivos .json no prefixo: bronze/raw_breweries/

---

## 🧪 Testes

Os testes cobrem:

Mock de boto3 e S3

Validação da transformação de dados

Verificação dos arquivos .parquet gerados

Comparação de DataFrame esperado com o resultado

Assertivas para verificar chamadas de upload no S3

Execute com:

pytest tests/
