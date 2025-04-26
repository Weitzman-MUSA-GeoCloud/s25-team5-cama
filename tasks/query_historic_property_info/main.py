import functions_framework
from google.cloud import bigquery
from flask import jsonify, request

# List of years to build historic values
YEARS = list(range(2016, 2025))

# Initialize BigQuery client globally
bigquery_client = bigquery.Client()

@functions_framework.http
def query_historic_property_info(request):
    # Get address query parameter
    address_query = request.args.get('address', '').lower().strip()

    if not address_query:
        return jsonify([]), 200  # Return empty list if no address provided

    # SQL query with parameter
    sql = """
        SELECT
          property_id,
          tax_year,
          market_value,
          market_value_2025,
          neighborhood,
          property_address,
          property_geog
        FROM
          derived.historic_year_property_assessment
        WHERE
          LOWER(property_address) LIKE @address_pattern
        ORDER BY
          property_id, tax_year
        LIMIT 10
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("address_pattern", "STRING", f"%{address_query}%")
        ]
    )

    query_job = bigquery_client.query(sql, job_config=job_config)
    results = query_job.result()

    # Build the property dictionary
    property_map = {}

    for row in results:
        property_id = str(row.property_id)

        if property_id not in property_map:
            property_map[property_id] = {
                "property_id": property_id,
                "neighborhood": str(row.neighborhood),
                "address": str(row.property_address),
                "geog": str(row.property_geog),
                "market_value_historic": {str(year): None for year in YEARS},
                "market_value_2025": int(row.market_value_2025) if row.market_value_2025 is not None else None
            }

        if 2016 <= row.tax_year <= 2024:
            property_map[property_id]["market_value_historic"][str(row.tax_year)] = int(row.market_value)

    # Output: list of property dicts
    properties_list = list(property_map.values())

    return jsonify(properties_list)
