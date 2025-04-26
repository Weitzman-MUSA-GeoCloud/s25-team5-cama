import functions_framework
from google.cloud import bigquery
from flask import jsonify, request, make_response

# Initialize BigQuery client globally
bigquery_client = bigquery.Client()


@functions_framework.http
def query_map_property_info(request):
    try:
        # Get address query parameter
        address_query = request.args.get('address', '').lower().strip()

        if not address_query:
            response = make_response(jsonify({}), 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        # Query exactly matching address
        query = """
            WITH base_data AS (
                SELECT
                  property_id,
                  MAX(market_value_2025) AS market_value_2025,
                  MAX(CASE WHEN tax_year = 2024 THEN market_value END) AS market_value_2024,
                  ANY_VALUE(neighborhood) AS neighborhood,
                  ANY_VALUE(property_address) AS property_address,
                  ANY_VALUE(property_geog) AS property_geog
                FROM
                  derived.historic_year_property_assessment
                GROUP BY
                  property_id
            )
            SELECT
              property_id,
              neighborhood,
              property_address,
              property_geog,
              market_value_2024,
              market_value_2025,
              (market_value_2025 - market_value_2024) AS change_absolute,
              ROUND(SAFE_DIVIDE((market_value_2025 - market_value_2024), market_value_2024), 2) AS change_percent,
              CASE
                WHEN (market_value_2025 - market_value_2024) > 0 THEN 'increase'
                WHEN (market_value_2025 - market_value_2024) = 0 THEN 'no_change'
                WHEN (market_value_2025 - market_value_2024) < 0 THEN 'decrease'
                ELSE NULL
              END AS change_type
            FROM base_data
            WHERE LOWER(property_address) = @exact_address
            LIMIT 1
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("exact_address", "STRING", address_query)
            ]
        )

        query_job = bigquery_client.query(query, job_config=job_config)
        results = list(query_job.result())

        if not results:
            response = make_response(jsonify({}), 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        row = results[0]

        property_data = {
            "property_id": str(row.property_id),
            "neighborhood": row.neighborhood,
            "address": row.property_address,
            "geog": row.property_geog,
            "market_value_2024": int(row.market_value_2024) if row.market_value_2024 is not None else None,
            "market_value_2025": int(row.market_value_2025) if row.market_value_2025 is not None else None,
            "change_absolute": int(row.change_absolute) if row.change_absolute is not None else None,
            "change_percent": float(row.change_percent) if row.change_percent is not None else None,
            "change_type": row.change_type
        }

        response = make_response(jsonify(property_data), 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except Exception as e:
        error_response = make_response(jsonify({"error": str(e)}), 500)
        error_response.headers['Access-Control-Allow-Origin'] = '*'
        return error_response
