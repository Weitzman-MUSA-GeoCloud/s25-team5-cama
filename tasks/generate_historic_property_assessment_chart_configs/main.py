import os
import functions_framework
import json
from google.cloud import storage
from google.cloud import bigquery
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DATA_DIR = Path(__file__).parent


@functions_framework.http
def generate_neighborhood_assessment_chart_configs(request):
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

        # Format the query results into a JSON structure
        json_data = []
        for row in results:
            json_data.append({
                "tax_year": int(row.tax_year),
                "lower_bound": int(row.lower_bound),
                "upper_bound": int(row.upper_bound),
                "property_count": int(row.property_count),
                "neighborhood": str(row.neighborhood)
            })

        if not json_data:
            continue

        # Generate the GCS blob name by replacing '.sql' with '.json'
        json_filename = filename.replace(".sql", ".json")
        blob_path = f"configs/{json_filename}"

        # Upload the JSON data to GCS
        blob = bucket.blob(blob_path)
        blob.upload_from_string(
            data=json.dumps(json_data, indent=2),
            content_type="application/json"
        )

    return "All configs generated and uploaded successfully.", 200
