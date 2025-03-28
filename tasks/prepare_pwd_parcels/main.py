import os
import json
import pathlib
import functions_framework
from google.cloud import storage
from dotenv import load_dotenv
load_dotenv()

DATA_DIR = pathlib.Path(__file__).parent


@functions_framework.http
def prepare_pwd_parcels(request):

    print('Preparing PWD Parcels data')

    raw_filename = DATA_DIR / 'pwd_parcels.geojson'
    prepared_filename = DATA_DIR / 'pwd_parcels.jsonl'

    bucket_name_raw = os.getenv('DATA_LAKE_BUCKET_RAW')
    storage_client = storage.Client()
    bucket_raw = storage_client.bucket(bucket_name_raw)

    # Download the raw data from the bucket
    raw_blobname = 'pwd_parcels/pwd_parcels.geojson'
    blob = bucket_raw.blob(raw_blobname)
    blob.download_to_filename(raw_filename)
    print(f'Downloaded to {raw_filename}')

    # Load the data from the GeoJSON file
    with open(raw_filename, 'r') as f:
        data = json.load(f)

    # Write the data to a JSONL file
    with open(prepared_filename, 'w') as f:
        for feature in data['features']:
            row = {k.lower(): v for k, v in feature['properties'].items()}  # convert keys to lowercase
            row['geog'] = (
                json.dumps(feature['geometry'])
                if feature['geometry'] and feature['geometry']['coordinates']
                else None
            )
            f.write(json.dumps(row) + '\n')

    print(f'Processed data into {prepared_filename}')

    bucket_name_prepare = os.getenv('DATA_LAKE_BUCKET_PREPARE')
    bucket_prepare = storage_client.bucket(bucket_name_prepare)

    # Upload the prepared data to the bucket
    prepared_blobname = 'pwd_parcels/data.jsonl'
    blob = bucket_prepare.blob(prepared_blobname)
    blob.upload_from_filename(prepared_filename)
    print(f'Uploaded to {prepared_blobname}')

    return f'Processed data into gs://{bucket_name_prepare}/{prepared_blobname}'
