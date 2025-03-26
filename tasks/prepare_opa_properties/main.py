import csv
import json
import os
import pathlib
import pyproj
from shapely import wkt
import functions_framework
from google.cloud import storage
from dotenv import load_dotenv
load_dotenv()

DATA_DIR = pathlib.Path(__file__).parent


@functions_framework.http
def prepare_opa_properties(request):

    print('Preparing OPA Properties data')

    raw_filename = DATA_DIR / 'opa_properties.csv'
    prepared_filename = DATA_DIR / 'opa_properties.jsonl'

    bucket_name_raw = os.getenv('DATA_LAKE_BUCKET_RAW')
    storage_client = storage.Client()
    bucket_raw = storage_client.bucket(bucket_name_raw)

    # Download the raw data from the bucket
    raw_blobname = 'opa_properties/opa_properties.csv'
    blob = bucket_raw.blob(raw_blobname)
    blob.download_to_filename(raw_filename)
    print(f'Downloaded to {raw_filename}')

    # Load the data from the CSV file
    with open(raw_filename, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # Set up the projection
    transformer = pyproj.Transformer.from_proj('epsg:2272', 'epsg:4326')

    # Write the data to a JSONL file
    with open(prepared_filename, 'w') as f:
        for i, row in enumerate(data):
            geom_wkt = row.pop('shape').split(';')[1]
            if geom_wkt == 'POINT EMPTY':
                row['geog'] = None
            else:
                geom = wkt.loads(geom_wkt)
                x, y = transformer.transform(geom.x, geom.y)
                row['geog'] = f'POINT({x} {y})'
            f.write(json.dumps(row) + '\n')

    print(f'Processed data into {prepared_filename}')

    bucket_name_prepare = os.getenv('DATA_LAKE_BUCKET_PREPARE')
    bucket_prepare = storage_client.bucket(bucket_name_prepare)

    # Upload the prepared data to the bucket
    prepared_blobname = 'opa_properties/data.jsonl'
    blob = bucket_prepare.blob(prepared_blobname)
    blob.upload_from_filename(prepared_filename)
    print(f'Uploaded to {prepared_blobname}')

    return f'Processed data into gs://{bucket_name_prepare}/{prepared_blobname}'
