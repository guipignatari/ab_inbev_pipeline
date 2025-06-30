# 🍻 AB InBev Data Pipeline (Medallion Architecture)

## 🎯 Objetivo

Este projeto implementa um pipeline de dados em três camadas (Bronze → Silver → Gold) utilizando Python, Pandas, PyArrow, S3 e Apache Airflow. Cada estágio do pipeline transforma os dados de forma incremental, culminando em agregações úteis para análise.

## 🌐 Fonte dos Dados

Este projeto utiliza dados reais disponibilizados por uma API pública:

https://www.openbrewerydb.org/

API: https://api.openbrewerydb.org/breweries

Os dados são extraídos no formato JSON e salvos na camada Bronze para posterior transformação e análise.

## 🚀 Stack Utilizada

- Python (pandas, boto3, pyarrow)
- AWS (S3, Athena, IAM)
- Airflow
- Docker / Docker Compose

## 📐 Arquitetura e Design

- **Camada Bronze:** ingestão bruta dos JSONs via API.
- **Silver:** limpeza e divisão por estado.
- **Gold:** agregações por tipo e estado.

## 📁 Estrutura de Pastas

![image](https://github.com/user-attachments/assets/127f4019-44b3-44e0-847b-8b69b7361067)

## ▶️ Como Executar Localmente

### Pré-requisitos

- Python 3.12+

Use o comando `pip install -r requirements.txt` para instalar as dependências.

### 🔐 Configuração das Credenciais AWS

Antes de executar o pipeline, é necessário configurar as credenciais da AWS para acessar o bucket S3. Siga os passos abaixo:

1. Obter credenciais na AWS
  
- Acesse o console da AWS: https://console.aws.amazon.com/iam/

- Vá até **IAM** (Identity and Access Management)

- Crie um novo usuário ou use um existente com permissão de acesso ao S3

- Ao criar o usuário, ative o acesso programático

- Conceda permissões como AmazonS3FullAccess ou uma política customizada

- Após a criação, você terá:

    - `AWS_ACCESS_KEY_ID`

    - `AWS_SECRET_ACCESS_KEY`

2. Criar o arquivo .env
   
Na raiz do projeto, crie um arquivo chamado `.env` com o seguinte conteúdo:

![image](https://github.com/user-attachments/assets/2c7ca1b8-321e-41f6-94dd-9fbec6b11103)

⚠️ Importante: Nunca suba esse arquivo para o Git. Ele já está incluído no .gitignore por padrão

Carregue-as no terminal com:

`set -a; source .env; set +a`

## ☁️ Configuração da Nuvem (AWS)

Crie um bucket S3: ab-inbev-data-pipeline

- Configure uma Role ou IAM User com permissões s3:PutObject, s3:GetObject, s3:ListBucket

- Adicione arquivos .json no prefixo: bronze/raw_breweries/

## ⚙️ Execução no Airflow

Cada camada possui uma DAG independente no Airflow:

| DAG              | Descrição                                               |
|------------------|---------------------------------------------------------|
| `bronze_dag.py`  | Ingestão dos arquivos JSON da camada Bronze (S3)        |
| `silver_dag.py`  | Processa e particiona dados por estado                  |
| `gold_dag.py`    | Realiza agregações por tipo e estado                    |

### 📦 Subindo o Airflow com Docker

1. **Inicie o ambiente Airflow com Docker Compose:**

```docker-compose up -d```

2. Acesse a interface do Airflow:

http://localhost:8080

 - Usuário padrão: `admin`
 - Senha padrão: `admin`

![image](https://github.com/user-attachments/assets/38d46b90-0124-4186-a942-8024e8203632)

## 📬 Monitoramento e Alertas

Cada DAG pode conter lógica de alerta via e-mail para falhas:

![image](https://github.com/user-attachments/assets/c66dc2fc-1310-4834-8cfa-fc109cb0b9bb)

## 🧪 Testes

Os testes implementados cobrem:

 - Validação da transformação de dados
 - Verificação dos arquivos .parquet gerados
 - Comparação de DataFrame esperado com o resultado
 - Assertivas para verificar chamadas de upload no S3

Execute no terminal com:

`pytest tests/`

## 👤 Autor

LinkedIn: [linkedin.com/in/guilhermepignatari](https://linkedin.com/in/guilhermepignatari)
GitHub: [github.com/guipignatari](https://github.com/guipignatari)
