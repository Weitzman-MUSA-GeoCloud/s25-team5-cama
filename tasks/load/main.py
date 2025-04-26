import os
import pathlib
import functions_framework
from google.cloud import bigquery
from dotenv import load_dotenv
load_dotenv()

DATA_DIR = pathlib.Path(__file__).parent


@functions_framework.http
def load_opa_assessments(request):
    return load_data('opa_assessments', request)


@functions_framework.http
def load_opa_properties(request):
    return load_data('opa_properties', request)


@functions_framework.http
def load_pwd_parcels(request):
    return load_data('pwd_parcels', request)


@functions_framework.http
def load_neighborhoods(request):
    return load_data('neighborhoods', request)


def load_data(table_name, request):
    sql_files = [f"source_{table_name}.sql", f"core_{table_name}.sql"]
    bigquery_client = bigquery.Client()

    for sql_filename in sql_files:
        # Read the SQL file specified in the request
        sql_path = DATA_DIR / sql_filename

        # Check that the file exists (else return 404 response from function i.e. not found)
        if (not sql_path.exists()) or (not sql_path.is_file()):
            # Return a 404 (not found) response if not
            return f'File {sql_path} not found', 404

        # Read the SQL file (if exists)
        print(f'Running {sql_path}')

        with open(sql_path, 'r', encoding='utf-8') as sql_file:  # encoding is utf8
            sql_query_template = sql_file.read()  # read file as a template because of ${} placeholders
            sql_query = render_template(  # process template with special functions
                sql_query_template,
                {
                    'bucket_name': os.getenv('DATA_LAKE_BUCKET_PREPARE'),
                    'dataset_name': os.getenv('DATA_LAKE_DATASET'),
                    'prepared_blobname': f'{table_name}/data.jsonl',
                    'table_name': table_name
                }
            )

        # Run the SQL query
        bigquery_client.query_and_wait(sql_query)

        print(f'Ran the SQL file {sql_path}')

    return 'Core table created'


def render_template(sql_query_template, context):
    clean_template = sql_query_template.replace('${', '{')
    return clean_template.format(**context)
