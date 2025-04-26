import pathlib
import functions_framework
from google.cloud import bigquery
from dotenv import load_dotenv
load_dotenv()

DATA_DIR = pathlib.Path(__file__).parent


@functions_framework.http
def model_to_table(request):
    bigquery_client = bigquery.Client()

    print('Starting query...')
    sql = '''
        CREATE OR REPLACE EXTERNAL TABLE source.current_year_assessment_value
        OPTIONS(
        format = 'csv',
        uris = ['gs://musa5090s25-team5-temp_data/model_output/model_output.csv']
        );

        DROP TABLE IF EXISTS derived.current_year_assessment_value;

        CREATE TABLE derived.current_year_assessment_value AS
        SELECT
            property_id,
            tax_year,
            round(sale_price_2025,0) AS sale_price_2025,
        FROM source.current_year_assessment_value;
    '''

    # Run the SQL query
    bigquery_client.query_and_wait(sql)

    print('Ran the SQL query')

    return 'Table updated!'
