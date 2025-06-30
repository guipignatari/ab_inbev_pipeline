# Imagem base
FROM python:3.9-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos para dentro do container
COPY . .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Comando padrão ao rodar o container
CMD ["python", "scripts/bronze_ingest.py"]