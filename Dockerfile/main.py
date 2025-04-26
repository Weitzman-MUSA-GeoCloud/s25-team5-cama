import json
from google.cloud import storage

# Create an empty GeoJSON FeatureCollection
empty_geojson = {
    "type": "FeatureCollection",
    "features": []
}

# Save to a local file
local_filename = "property_tile_info.geojson"
with open(local_filename, "w") as f:
    json.dump(empty_geojson, f, indent=4)

# Upload to GCP `temp_data` bucket
bucket_name = "musa5090s25-team5-temp_data"
client = storage.Client()
bucket = client.bucket(bucket_name)
blob = bucket.blob(local_filename)
blob.upload_from_filename(local_filename)

print(f"Uploaded empty GeoJSON to gs://{bucket_name}/{local_filename}")