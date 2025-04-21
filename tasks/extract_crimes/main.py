import os
import pathlib
import requests
import functions_framework
from google.cloud import storage
from dotenv import load_dotenv
load_dotenv()

DATA_DIR = pathlib.Path(__file__).parent


@functions_framework.http
def extract_crimes(request):

    print('Extracting 2024 crimes data')

    # Download the crimes data as a CSV
    url = 'https://phl.carto.com/api/v2/sql?filename=incidents_part1_part2&format=csv&q=SELECT%20*%20,%20ST_Y(the_geom)%20AS%20lat,%20ST_X(the_geom)%20AS%20lng%20FROM%20incidents_part1_part2%20WHERE%20dispatch_date_time%20%3E=%20%272024-01-01%27%20AND%20dispatch_date_time%20%3C%20%272025-01-01%27'
    filename = DATA_DIR / 'crimes.csv'

    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as f:
        f.write(response.content)

    print(f'Downloaded {filename}')

    # Upload the downloaded file to cloud storage
    bucket_name = os.getenv('DATA_LAKE_BUCKET_RAW')
    blobname = 'crimes/crimes.csv'

    # For now we will overwrite the file each time we run the script
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blobname)
    blob.upload_from_filename(filename)

    print(f'Uploaded {blobname} to {bucket_name}')

    return f'Downloaded and uploaded gs://{bucket_name}/{blobname}'
