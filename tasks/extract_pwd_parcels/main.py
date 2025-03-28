import os
import pathlib
import requests
import functions_framework
from google.cloud import storage
from dotenv import load_dotenv
load_dotenv()

DATA_DIR = pathlib.Path(__file__).parent


@functions_framework.http
def extract_pwd_parcels(request):

    print('Extracting PWD Parcels data')

    # Download the PWD parcels data as a geojson
    url = 'https://www.pasda.psu.edu/json/PhillyWater_PWD_PARCELS2025.geojson'
    # 'https://opendata.arcgis.com/datasets/84baed491de44f539889f2af178ad85c_0.geojson'
    filename = DATA_DIR / 'pwd_parcels.geojson'

    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as f:
        f.write(response.content)

    print(f'Downloaded {filename}')

    # Upload the downloaded file to cloud storage
    bucket_name = os.getenv('DATA_LAKE_BUCKET_RAW')
    blobname = 'pwd_parcels/pwd_parcels.geojson'

    # For now we will overwrite the file each time we run the script
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blobname)
    blob.upload_from_filename(filename)

    print(f'Uploaded {blobname} to {bucket_name}')

    return f'Downloaded and uploaded gs://{bucket_name}/{blobname}'
