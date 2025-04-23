import json
import functions_framework
from google.cloud import bigquery
from google.cloud import storage


@functions_framework.http
def property_tiles_info(request):
    bigquery_client = bigquery.Client()

    print('Starting query...')
    sql = '''
        SELECT
            property.property_id        AS property_id,
            property.property_address   AS address,
            property.market_value       AS tax_year_assessed_value,
            property.market_value_2025  AS current_assessed_value,
            property.neighborhood       AS neighborhood,
            parcel.geog                 AS geometry
        FROM derived.historic_year_property_assessment AS property
        JOIN source.pwd_parcels    AS parcel
            ON CAST(parcel.BRT_ID AS INTEGER) = property.property_id
        WHERE property.tax_year = 2024
    '''

    query_results = bigquery_client.query_and_wait(sql)
    rows = list(query_results)
    print('Finished query.')

    features = []
    for row in rows:
        features.append({
            'type': 'Feature',
            'properties': {
                'property_id': row['property_id'],
                'address': row['address'],
                'tax_year_assessed_value': row['tax_year_assessed_value'],
                'current_assessed_value': row['current_assessed_value'],
                'neighborhood': row['neighborhood'],
            },
            'geometry': json.loads(row['geometry'])
        })

    feature_collection = {
        'type': 'FeatureCollection',
        'features': features
    }

    geojson = json.dumps(feature_collection)

    print('Uploading to GCS...')
    storage_client = storage.Client()
    bucket = storage_client.bucket('musa5090s25-team5-temp_data')
    blob = bucket.blob('property_tile_info.geojson')
    blob.upload_from_string(geojson)
    print('Finished uploading.')

    return 'Success!'
