import pathlib
import functions_framework
from google.cloud import bigquery

# Directory where the SQL files are stored (same folder as this script)
DATA_DIR = pathlib.Path(__file__).parent


@functions_framework.http
def create_distribution_table(request):
    sql_files = [
        "create_derived_current_year_neighborhood_assessment_bins.sql",
        "create_derived_current_year_philadelphia_assessment_bins.sql",
        "create_derived_tax_year_neighborhood_assessment_bins.sql",
        "create_derived_tax_year_philadelphia_assessment_bins.sql"
    ]

    bigquery_client = bigquery.Client()

    for filename in sql_files:
        sql_path = DATA_DIR / filename

        if not sql_path.exists():
            return f"SQL file not found: {sql_path}", 404

        print(f"Running: {sql_path.name}")

        with open(sql_path, "r", encoding="utf-8") as f:
            sql = f.read()

        bigquery_client.query(sql).result()  # Wait until the query completes

        print(f"Finished: {sql_path.name}")

    return "All SQL scripts executed successfully."
