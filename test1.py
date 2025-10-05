import requests

response = requests.get(
    "https://catalog.api.2gis.com/3.0/markers?q=кафе&point=37.545423%2C55.740693&radius=500&location=37.545423%2C55.740693&sort=distance&key=2dfc0b30-cdb7-4014-9142-4d101cb77824"
)
print(response.json())
