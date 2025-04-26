from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Load property data from GCS public URL
GCS_JSON_URL = 'https://storage.googleapis.com/musa5090s25-team5-public/configs/chart_historic_year_property.json'

response = requests.get(GCS_JSON_URL)
if response.status_code == 200:
    property_data = response.json()
else:
    raise Exception(f"Failed to load property data from GCS, status code: {response.status_code}")

@app.route('/queryProperty', methods=['GET'])
def query_property():
    query = request.args.get('address', '').lower().strip()
    if not query:
        return "Address query parameter is required.", 400

    matches = []
    for property_id, property_info in property_data.items():
        address = property_info.get('address', '').lower()
        if query in address:
            full_property = {
                "propertyId": property_id,
                **property_info
            }
            matches.append(full_property)
            if len(matches) >= 5:
                break

    return jsonify(matches)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
