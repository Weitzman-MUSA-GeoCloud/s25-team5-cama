import csv
import json
import os
import pathlib
import functions_framework
from google.cloud import storage
from dotenv import load_dotenv
load_dotenv()

DATA_DIR = pathlib.Path(__file__).parent


@functions_framework.http
def prepare_opa_assessments(request):

    print('Preparing OPA Assessments data')

    raw_filename = DATA_DIR / 'opa_assessments.csv'
    prepared_filename = DATA_DIR / 'opa_assessments.jsonl'

    bucket_name_raw = os.getenv('DATA_LAKE_BUCKET_RAW')
    storage_client = storage.Client()
    bucket_raw = storage_client.bucket(bucket_name_raw)

    # Download the raw data from the bucket
    raw_blobname = 'opa_assessments/opa_assessments.csv'
    blob = bucket_raw.blob(raw_blobname)
    blob.download_to_filename(raw_filename)
    print(f'Downloaded to {raw_filename}')

    # Load the data from the CSV file
    with open(raw_filename, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # Write the data to a JSONL file
    with open(prepared_filename, 'w') as f:
        for row in data:
            f.write(json.dumps(row) + '\n')

    print(f'Processed data into {prepared_filename}')

    bucket_name_prepare = os.getenv('DATA_LAKE_BUCKET_PREPARE')
    bucket_prepare = storage_client.bucket(bucket_name_prepare)

    # Upload the prepared data to the bucket
    prepared_blobname = 'opa_assessments/data.jsonl'
    blob = bucket_prepare.blob(prepared_blobname)
    blob.upload_from_filename(prepared_filename)
    print(f'Uploaded to {prepared_blobname}')

    return f'Processed data into gs://{bucket_name_prepare}/{prepared_blobname}'
