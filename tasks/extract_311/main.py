import os
import pathlib
import requests
import functions_framework
from google.cloud import storage
from dotenv import load_dotenv
load_dotenv()

DATA_DIR = pathlib.Path(__file__).parent


@functions_framework.http
def extract_311(request):

    print('Extracting 311 requests data')

    # Download the 311 requests 2024 data as a CSV
    url = 'https://phl.carto.com/api/v2/sql?filename=public_cases_fc&format=csv&skipfields=cartodb_id,the_geom,the_geom_webmercator&q=SELECT%20*%20FROM%20public_cases_fc%20WHERE%20requested_datetime%20%3E=%20%272024-01-01%27%20AND%20requested_datetime%20%3C%20%272025-01-01%27'
    filename = DATA_DIR / '311.csv'

    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as f:
        f.write(response.content)

    print(f'Downloaded {filename}')

    # Upload the downloaded file to cloud storage
    bucket_name = os.getenv('DATA_LAKE_BUCKET_RAW')
    blobname = '311/311.csv'

    # For now we will overwrite the file each time we run the script
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blobname)
    blob.upload_from_filename(filename)

    print(f'Uploaded {blobname} to {bucket_name}')

    return f'Downloaded and uploaded gs://{bucket_name}/{blobname}'
