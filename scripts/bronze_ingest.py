import requests
import boto3
import datetime
import json
from io import BytesIO

# Configurações
API_URL = "https://api.openbrewerydb.org/v1/breweries"
BUCKET_NAME = "ab-inbev-data-pipeline"
BRONZE_PREFIX = "bronze/raw_breweries"

# 1. Obtem dados da API
response = requests.get(API_URL)
response.raise_for_status()
data = response.json()

# 2. Converte para bytes (em formato JSON)
json_data = json.dumps(data, indent=2)
bytes_buffer = BytesIO(json_data.encode('utf-8'))

# 3. Nome do arquivo com timestamp
timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
file_key = f"{BRONZE_PREFIX}/brewery_data_{timestamp}.json"

# 4. Envia para o S3
s3 = boto3.client('s3')
s3.upload_fileobj(bytes_buffer, BUCKET_NAME, file_key)

print(f"✅ Arquivo enviado para S3: s3://{BUCKET_NAME}/{file_key}")