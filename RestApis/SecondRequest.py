import os
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import tarfile
import json
import io

# Your client credentials
client_id = 'sh-c5b16fdb-00ee-4a3e-a8c9-a904bb1c23ac'
client_secret = 'gGRSaOPuwWaGc7YWDULsmaTgB4Yj4KOU'

# Create a session
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)

# Get token for the session
token = oauth.fetch_token(token_url='https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token',
                          client_secret=client_secret, include_client_id=True)

# All requests using this session will have an access token automatically added
# resp = oauth.get("...")
# print(resp.content)

evalscript = """
//VERSION=3
function setup() {
  return {
    input: ["VV"],
    output: { id: "default", bands: 1 },
  }
}

function evaluatePixel(samples) {
  return [2 * samples.VV]
}
"""

request = {
    "input": {
        "bounds": {
            "bbox": [
                1360000,
                5121900,
                1370000,
                5131900,
            ],
            "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/3857"},
        },
        "data": [
            {
                "type": "sentinel-1-grd",
                "dataFilter": {
                    "timeRange": {
                        "from": "2023-02-02T00:00:00Z",
                        "to": "2023-04-02T23:59:59Z",
                    }
                },
                "processing": {"orthorectify": "true"},
            }
        ],
    },
    "output": {
        "width": 512,
        "height": 512,
        "responses": [
            {
                "identifier": "default",
                "format": {"type": "image/png"},
            }
        ],
    },
    "evalscript": evalscript,
}

url = "https://sh.dataspace.copernicus.eu/api/v1/process"
response = oauth.post(url, json=request)

# Check if the response was successful
if response.status_code == 200:
    # Create the directory if it doesn't exist
    os.makedirs("Sentinel_1", exist_ok=True)
    # Write the binary content of the response to a file
    destination_file_name = "Sentinel_1/S3OLCI_Example1.png"
    with open(destination_file_name, 'wb') as file:
        file.write(response.content)
    print("Image saved")
else:
    print("Error:", response.status_code, response.text)
