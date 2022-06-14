
import requests

url = "https://earthquake.usgs.gov/fdsnws/event/1/query?"
format_header = {'accept': 'application/json'}
params_json = {'format': 'geojson',
               'starttime': '2022-01-01',
               'endtime': '2022-05-05',
               'latitude': '50.45',
               'longitude': '30.52',
               'maxradiuskm': '1000'
               }
zvit = requests.get(url, headers=format_header, params=params_json)

# print(zvit.text)
# print(type(zvit.json()))
# response = requests.get(url, headers={'accept': 'application/json'})
# print(response.text)
data = zvit.json()
print(data['features'][3]['geometry']['coordinates'])
