import os
import pathlib
import functions_framework
from google.cloud import bigquery
from dotenv import load_dotenv
load_dotenv()

DATA_DIR = pathlib.Path(__file__).parent


@functions_framework.http
def load_opa_assessments(request):

    # Read the SQL file specified in the request (from query string paramter)
    sql_path = DATA_DIR / 'source_opa_assessments.sql'

    # Check that the file exists (else return 404 response from function i.e. not found)
    if (not sql_path.exists()) or (not sql_path.is_file()):
        # Return a 404 (not found) response if not
        return f'File {sql_path} not found', 404

    # Read the SQL file (if exists)
    print('Extracting OPA Assessments data')

    with open(sql_path, 'r', encoding='utf-8') as sql_file:  # encoding is utf8
        sql_query_template = sql_file.read()  # read file as a template because of ${} placeholders
        sql_query = render_template(  # process template with special functions
            sql_query_template,
            {
                'bucket_name': os.getenv('DATA_LAKE_BUCKET_PREPARE'),
                'dataset_name': os.getenv('DATA_LAKE_DATASET'),
                'prepared_blobname': 'opa_assessments/data.jsonl',
                'table_name': 'opa_assessments'
            }
        )

    # Run the SQL query
    bigquery_client = bigquery.Client()
    bigquery_client.query_and_wait(sql_query)

    print(f'Ran the SQL file {sql_path} to load table')

    return f'Ran the SQL file {sql_path} to load table'

def render_template(sql_query_template, context):
    clean_template = sql_query_template.replace('${', '{')
    return clean_template.format(**context)
