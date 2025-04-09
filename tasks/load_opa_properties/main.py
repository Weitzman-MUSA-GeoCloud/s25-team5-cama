import os
import pathlib
import functions_framework
from google.cloud import bigquery
from dotenv import load_dotenv
load_dotenv()

DATA_DIR = pathlib.Path(__file__).parent


@functions_framework.http
def load_opa_properties(request):

    sql_files = ["source_opa_properties.sql", "core_opa_properties.sql"]
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
                    'prepared_blobname': 'opa_properties/data.jsonl',
                    'table_name': 'opa_properties'
                }
            )

        # Run the SQL query
        bigquery_client.query_and_wait(sql_query)

        print(f'Ran the SQL file {sql_path}')

    return 'Core table created'


def render_template(sql_query_template, context):
    clean_template = sql_query_template.replace('${', '{')
    return clean_template.format(**context)
