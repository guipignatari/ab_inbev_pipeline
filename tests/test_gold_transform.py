import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from scripts import gold_transform
from io import BytesIO
from pyarrow import parquet as pq

@patch("scripts.gold_transform.list_parquet_files", return_value=["silver/silver_breweries/CA.parquet"])
@patch("scripts.gold_transform.read_parquet_from_s3")
@patch("scripts.gold_transform.boto3.client")
def test_gold_transform_and_save(mock_boto_client, mock_read_parquet, mock_list_files):
    # Mock dos dados simulando os arquivos da camada Silver
    sample_df = pd.DataFrame({
        "brewery_type": ["micro", "micro", "nano", "brewpub"],
        "state": ["CA", "CA", "CA", "CA"]
    })

    # Mock read_parquet para retornar o DataFrame
    mock_read_parquet.return_value = sample_df

    # Criação do mock para boto3 e método put_object
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3
    # Executa a função principal da transformação Gold
    gold_transform.transform_and_save()

    # Verifica se o upload foi chamado
    assert mock_s3.put_object.called, "O upload para o S3 não foi chamado."

    # Valida o conteúdo do arquivo Parquet enviado
    args, kwargs = mock_s3.put_object.call_args
    uploaded_buffer = BytesIO(kwargs["Body"])
    uploaded_buffer.seek(0)
    result_df = pq.read_table(uploaded_buffer).to_pandas()

    # DataFrame esperado após a agregação
    expected_df = pd.DataFrame({
        "brewery_type": ["brewpub", "micro", "nano"],
        "state": ["CA", "CA", "CA"],
        "brewery_count": [1, 2, 1]
    })

    # Compara os DataFrames
    pd.testing.assert_frame_equal(
        result_df.sort_values(by=["brewery_type"]).reset_index(drop=True),
        expected_df.sort_values(by=["brewery_type"]).reset_index(drop=True)
    )
