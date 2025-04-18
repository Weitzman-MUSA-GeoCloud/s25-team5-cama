import os
import functions_framework
import json
from google.cloud import storage
from google.cloud import bigquery
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DATA_DIR = Path(__file__).parent

# List of years to process
YEARS = list(range(2016, 2025))


@functions_framework.http
def generate_historic_property_assessment_chart_configs(request):
    # List of SQL files to process
    sql_files = [
        "chart_historic_year_property.sql",
    ]

    bigquery_client = bigquery.Client()
    storage_client = storage.Client()

    bucket_name = os.getenv('DATA_LAKE_BUCKET_PUBLIC')
    bucket = storage_client.bucket(bucket_name)

    for filename in sql_files:
        # Read SQL query from file
        sql_path = DATA_DIR / filename
        with open(sql_path, "r", encoding="utf-8") as f:
            sql = f.read()

        # Execute the query
        query_job = bigquery_client.query(sql)
        results = query_job.result()

        # Initialize the result dictionary
        property_dict = {}

        for row in results:
            property_id = str(row.property_id)

            # Initialize property entry if not already created
            if property_id not in property_dict:
                property_dict[property_id] = {
                    "neighborhood": str(row.neighborhood),
                    "address": str(row.property_address),
                    "geog": str(row.geog),
                    "market_value_historic": {str(year): None for year in YEARS},
                    "market_value_2025": int(row.market_value_2025) if row.market_value_2025 is not None else None
                }

            # Assign market value for historic years
            if 2016 <= row.tax_year <= 2024:
                property_dict[property_id]["market_value_historic"][str(row.tax_year)] = int(row.market_value)

        # Generate the GCS blob name by replacing '.sql' with '.json'
        json_filename = filename.replace(".sql", ".json")
        blob_path = f"configs/{json_filename}"

        # Upload the JSON data to GCS
        blob = bucket.blob(blob_path)
        blob.upload_from_string(
            data=json.dumps(property_dict, indent=2),
            content_type="application/json"
        )

    return "All configs generated and uploaded successfully.", 200
