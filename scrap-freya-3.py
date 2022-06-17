

from bs4 import BeautifulSoup
import requests
import csv


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36\
         (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
image_number = 0
page_number = 1
link_site = 'https://cosmohit.ua'
link_site_ua = 'https://ua.cosmohit.ua'
link_catalog = 'https://cosmohit.ua/catalogue/cosmetics/'

response = requests.get(link_catalog, headers=headers).text
soup = BeautifulSoup(response, 'lxml')
max_pages = soup.select_one('.paginator > a:nth-child(5)').get_text()
nomer = 0

with open('112.csv', 'w', encoding='utf-8') as file:
    field_names = ['nomer', 'name', 'name2', 'name_original', 'price']
    csv_writer = csv.DictWriter(file, fieldnames=field_names)

    for page in range(1):  # 1, int(max_pages)
        response_page = requests.get(f'{link_catalog}page/{page}', headers=headers).text
        soup_page = BeautifulSoup(response_page, 'lxml')
        link_product = soup_page.select('.items > div > a')
        # print(page)
        for link in link_product:
            url_href = link.get('href')
            response_tovar = requests.get(f'{link_site}{url_href}', headers=headers).text
            soup_link = BeautifulSoup(response_tovar, 'lxml')

            name_tovar_span = soup_link.select_one('.item_layout>ul:first-child>li:nth-child(2)>div:last-child>span').text
            print(name_tovar_span)

            name_tovar = soup_link.select_one('.item_layout>ul:first-child>li:nth-child(2)>div:last-child')
            name_tovar.span.decompose()
            name_tovar_en = name_tovar.text.replace('"', '')
            print(name_tovar_en)

            price = soup_link.find(itemprop="price").get('content')
            print(price)

            response_tovar_ua = requests.get(f'{link_site_ua}{url_href}', headers=headers).text
            soup_link_ua = BeautifulSoup(response_tovar_ua, 'lxml')
            name_tovar_span_ua = soup_link_ua.select_one('.item_layout>ul:first-child>li:nth-child(2)>div:last-child>span').text
            print(name_tovar_span_ua)

            nomer += 1

            csv_writer.writerow({
                'nomer': nomer,
                'name': name_tovar_span,
                'name2': name_tovar_span_ua,
                'name_original': name_tovar_en,
                'price': price
             })



        # name2 = name_tovar.span.decompose()
        # print(name2)
    # link_product_href = link_product.get()

    # print(f'{link}page/{page}')



# response = requests.get(link, headers=headers)

# print(response.status_code)

# response = response.text
# print(response)

# soup = BeautifulSoup(response, 'lxml')
# all_image =
# for image in soup:
#     asd = image
