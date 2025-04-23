import os
import pathlib
import requests
import functions_framework
from google.cloud import storage
from dotenv import load_dotenv
load_dotenv()

DATA_DIR = pathlib.Path(__file__).parent


@functions_framework.http
def extract_neighborhoods(request):

    print('Extracting Neighborhoods data')

    # Download the Neighborhoods data as a geojson
    url = 'https://raw.githubusercontent.com/opendataphilly/open-geo-data/refs/heads/master/philadelphia-neighborhoods/philadelphia-neighborhoods.geojson'
    filename = DATA_DIR / 'neighborhoods.geojson'

    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as f:
        f.write(response.content)

    print(f'Downloaded {filename}')

    # Upload the downloaded file to cloud storage
    bucket_name = os.getenv('DATA_LAKE_BUCKET_RAW')
    blobname = 'neighborhoods/neighborhoods.geojson'

    # For now we will overwrite the file each time we run the script
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blobname)
    blob.upload_from_filename(filename)
    print('Uploaded to raw bucket')

    # Also upload to public bucket
    bucket_name_public = os.getenv('DATA_LAKE_BUCKET_PUBLIC')
    bucket_public = storage_client.bucket(bucket_name_public)
    blob2 = bucket_public.blob(blobname)
    blob2.upload_from_filename(filename)
    print('Uploaded to public bucket')

    return f'Downloaded and uploaded into [gs://{bucket_name}/{blobname}] and [gs://{bucket_name_public}/{blobname}]'
