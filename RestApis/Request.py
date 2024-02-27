import requests

# Define the search parameters
data = {
    "bbox": [13, 45, 14, 46],
    "datetime": "2019-12-10T00:00:00Z/2019-12-10T23:59:59Z",
    "collections": ["sentinel-1-grd"],
    "limit": 5,
}

url = "https://sh.dataspace.copernicus.eu/api/v1/catalog/1.0.0/search"

response = requests.post(url, json=data)

if response.status_code == 200:
    print(response.json())
else:
    print("Error:", response.status_code)
