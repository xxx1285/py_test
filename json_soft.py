

import requests

url = "https://earthquake.usgs.gov/fdsnws/event/1/query?"
header_type = {'accept': 'application/json'}

start_time = input('Input starttime: ')
end_time = input('Input endtime: ')
latitude = input('Input latitude: ')
longitude = input('Input longitude: ')
maxradiuskm = input('Input maxradiuskm: ')

params_json = {'format': 'geojson',
               'starttime': start_time,
               'endtime': end_time,
               'latitude': latitude,
               'longitude': longitude,
               'maxradiuskm': maxradiuskm
               }
zvit = requests.get(url, headers=header_type, params=params_json)

data = zvit.json()
param_data = data['features']
count = 0

for param in param_data:
    count += 1
    print(f'{count}. Last land magnitud bila {param["properties"]["place"]}\
        so hard {param["properties"]["mag"]}')
