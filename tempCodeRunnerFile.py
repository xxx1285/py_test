

from bs4 import BeautifulSoup
# from transliterate import slugify
import requests
# import csv
# import os

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
link_site_ua = 'https://mixmebli.com/catalogs'
# link_catalog = 'https://constanta.ua/56-krisla-ta-pufi?p='

image_number = 0
nomer = 0

response = requests.get(link_site_ua, headers=headers).text
soup = BeautifulSoup(response, 'lxml')

all_category_in_catalog = soup.select(".category-wall .caption a")

for category in all_category_in_catalog:
    url_category = category.get('href')

    response_url_category = requests.get(url_category, headers=headers).text
    soup_url_category = BeautifulSoup(response_url_category, 'lxml')

    all_tovars_in_category = soup_url_category.select(".product-block .name a")
    print(all_tovars_in_category)