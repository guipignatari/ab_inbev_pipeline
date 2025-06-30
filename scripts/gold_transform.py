import os
import boto3
import pandas as pd
from io import BytesIO
import pyarrow.parquet as pq
from pyarrow import Table

def list_parquet_files(bucket, prefix):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    return [
        content['Key']
        for content in response.get('Contents', [])
        if content['Key'].endswith('.parquet')
    ]

def read_parquet_from_s3(bucket, key):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=key)
    return pd.read_parquet(BytesIO(obj['Body'].read()))

def transform_and_save():
    bucket = os.getenv('S3_BUCKET')
    silver_prefix = 'silver/silver_breweries/'
    gold_prefix = 'gold/gold_breweries/'

    # List and read all parquet files from silver layer
    parquet_files = list_parquet_files(bucket, silver_prefix)
    df_list = [read_parquet_from_s3(bucket, key) for key in parquet_files]
    df = pd.concat(df_list, ignore_index=True)

    # Aggregate: count breweries by type and state
    agg_df = df.groupby(['brewery_type', 'state']).size().reset_index(name='brewery_count')

    # Convert to Parquet
    table = Table.from_pandas(agg_df)
    buffer = BytesIO()
    pq.write_table(table, buffer)
    buffer.seek(0)

    # Save back to S3
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket, Key=f'{gold_prefix}brewery_aggregates.parquet', Body=buffer.getvalue())

if __name__ == "__main__":
    transform_and_save()
