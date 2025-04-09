import os
import functions_framework
import json
from google.cloud import storage
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()


@functions_framework.http
def generate_assessment_chart_configs(request):
    # Step 1: Query the BigQuery table
    query = """
        SELECT
          tax_year,
          lower_bound,
          upper_bound,
          property_count
        FROM
          derived.tax_year_assessment_bins
        ORDER BY lower_bound
    """

    bigquery_client = bigquery.Client()
    query_job = bigquery_client.query(query)
    results = query_job.result()

    # Step 2: Convert results to JSON
    json_data = []
    for row in results:
        json_data.append({
            "tax_year": row.tax_year,
            "lower_bound": int(row.lower_bound),
            "upper_bound": int(row.upper_bound),
            "property_count": int(row.property_count)
        })

    # Step 3: Upload to GCS
    bucket_name = os.getenv('DATA_LAKE_BUCKET_CONFIG')
    blobname = "tax_year_assessment_bins.json"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blobname)

    blob.upload_from_string(
        data=json.dumps(json_data, indent=2),
        content_type="application/json"
    )

    return (
        "2024 assessment distribution chart config generated and uploaded.",
        200
    )
