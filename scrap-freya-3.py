import requests
import re
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36\
         (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
page_number = 1
link = f'https://cosmohit.ua/catalogue/cosmetics/page/{page_number}'

response = requests.get(link, headers=headers).text
soup = BeautifulSoup(response, 'lxml')


block = soup.find('div', class_='items')
all_images = block.find_all('div', class_=re.compile("item_"))

for image in all_images:
    image_link = image.find('a').get('href')
    print(image)
    print('\n\n')
