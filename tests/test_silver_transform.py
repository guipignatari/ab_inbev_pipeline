import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from scripts import silver_transform

def test_transform_and_save(monkeypatch):
    # Mock da lista de arquivos no bucket Bronze
    monkeypatch.setattr(silver_transform, "list_json_files", lambda: ["bronze/raw_breweries/sample.json"])

    # Mock do cliente boto3 e do retorno do método get_object
    mock_s3 = MagicMock()
    sample_data = pd.DataFrame([
        {"id": 1, "name": "Brew A", "state": "CA", "brewery_type": "micro"},
        {"id": 2, "name": "Brew B", "state": "NY", "brewery_type": "nano"},
    ])
    # Transforma o DataFrame em JSON e simula o conteúdo vindo do S3
    json_bytes = sample_data.to_json(orient="records").encode("utf-8")
    mock_s3.get_object.return_value = {"Body": pd.io.common.BytesIO(json_bytes)}
    # Substitui o cliente S3 real pelo mock
    monkeypatch.setattr(silver_transform, "s3", mock_s3)

    # Mock do método de upload de arquivos
    mock_s3.upload_fileobj = MagicMock()

    # Executa a função de transformação
    silver_transform.transform_and_save()

    # Verifica se o upload foi realmente chamado
    assert mock_s3.upload_fileobj.called
