import os
import pathlib
import functions_framework
from google.cloud import bigquery
from dotenv import load_dotenv
load_dotenv()

DATA_DIR = pathlib.Path(__file__).parent


@functions_framework.http
def load_opa_assessments(request):

    print('Extracting OPA Assessments data')

    bucket_name = os.getenv('DATA_LAKE_BUCKET_PREPARE')
    dataset_name = os.getenv('DATA_LAKE_DATASET')

    # Load the data into BigQuery as an external table
    prepared_blobname = 'opa_assessments/data.jsonl'
    table_name = 'opa_assessments'
    table_uri = f'gs://{bucket_name}/{prepared_blobname}'

    create_table_query = f'''
    CREATE OR REPLACE EXTERNAL TABLE {dataset_name}.{table_name}
    OPTIONS(
        format = 'JSON',
        uris = ['{table_uri}']
    )
    '''
    print(create_table_query)

    bigquery_client = bigquery.Client()
    # print(bigquery_client._credentials.service_account_email)
    bigquery_client.query_and_wait(create_table_query)

    print(f'Loaded {table_uri} into {dataset_name}.{table_name}')

    return f'Loaded {table_uri} into {dataset_name}.{table_name}'
