import os
import pathlib
import requests
import functions_framework
from google.cloud import storage
from dotenv import load_dotenv
load_dotenv()

DATA_DIR = pathlib.Path(__file__).parent


@functions_framework.http
def extract_opa_properties(request):

    print('Extracting OPA Properties data')

    # Download the OPA Properties data as a CSV
    url = 'https://opendata-downloads.s3.amazonaws.com/opa_properties_public.csv'
    filename = DATA_DIR / 'opa_properties.csv'

    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as f:
        f.write(response.content)

    print(f'Downloaded {filename}')

    # Upload the downloaded file to cloud storage
    bucket_name = os.getenv('DATA_LAKE_BUCKET_RAW')
    blobname = 'opa_properties/opa_properties.csv'

    # For now we will overwrite the file each time we run the script
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blobname)
    blob.upload_from_filename(filename)

    print(f'Uploaded {blobname} to {bucket_name}')

    return f'Downloaded and uploaded gs://{bucket_name}/{blobname}'
