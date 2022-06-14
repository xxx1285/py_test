

import requests

url = "https://antydot.info/"

response = requests.get(url)

print(f'requesrs to {url}. Status code is {response.status_code}.')
print(response.text)