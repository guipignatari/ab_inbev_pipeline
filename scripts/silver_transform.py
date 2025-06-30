import os
import boto3
import pandas as pd
from io import BytesIO
import pyarrow as pa
import pyarrow.parquet as pq
from dotenv import load_dotenv

AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_REGION = os.environ["AWS_DEFAULT_REGION"]
BUCKET_NAME = os.environ["S3_BUCKET"]

bronze_prefix = "bronze/raw_breweries/"
silver_prefix = "silver/silver_breweries/"

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

def list_json_files():
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=bronze_prefix)
    return [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.json')]

def transform_and_save():
    files = list_json_files()

    for key in files:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        raw_data = pd.read_json(obj['Body'])
        raw_data.dropna(subset=["state", "id", "name"], inplace=True)

        grouped = raw_data.groupby("state")

        for state, df in grouped:
            table = pa.Table.from_pandas(df)
            buffer = BytesIO()
            pq.write_table(table, buffer)
            buffer.seek(0)

            output_key = f"{silver_prefix}{state}/brewery_data.parquet"
            s3.upload_fileobj(buffer, BUCKET_NAME, output_key)
            print(f"✅ Saved: {output_key}")

if __name__ == "__main__":
    transform_and_save()
