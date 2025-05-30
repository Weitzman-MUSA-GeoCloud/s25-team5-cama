import functions_framework
from google.cloud import bigquery
from flask import jsonify, request, make_response

# List of years to build historic values
YEARS = list(range(2016, 2025))

# Initialize BigQuery client globally
bigquery_client = bigquery.Client()


@functions_framework.http
def query_historic_property_info(request):
    try:
        # Get address query parameter
        address_query = request.args.get('address', '').lower().strip()

        if not address_query:
            response = make_response(jsonify([]), 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        # Step 1: First query - get up to 6 distinct property_ids
        property_id_sql = """
            SELECT DISTINCT property_id
            FROM derived.historic_year_property_assessment
            WHERE LOWER(property_address) LIKE @address_pattern
            ORDER BY property_id
            LIMIT 6
        """

        property_id_job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("address_pattern", "STRING", f"%{address_query}%")
            ]
        )

        property_id_query_job = bigquery_client.query(property_id_sql, job_config=property_id_job_config)
        property_id_results = property_id_query_job.result()

        property_ids = [int(row.property_id) for row in property_id_results]

        if not property_ids:
            response = make_response(jsonify([]), 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        # Step 2: Second query - get full details for those property_ids
        property_detail_sql = """
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
            WHERE property_id IN UNNEST(@property_ids)
            ORDER BY property_id, tax_year
        """

        property_detail_job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ArrayQueryParameter("property_ids", "INT64", property_ids)
            ]
        )

        property_detail_query_job = bigquery_client.query(property_detail_sql, job_config=property_detail_job_config)
        results = property_detail_query_job.result()

        # Step 3: Build the property dictionary
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

        properties_list = list(property_map.values())

        response = make_response(jsonify(properties_list), 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except Exception as e:
        error_response = make_response(jsonify({"error": str(e)}), 500)
        error_response.headers['Access-Control-Allow-Origin'] = '*'
        return error_response
