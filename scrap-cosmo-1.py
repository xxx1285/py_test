

from bs4 import BeautifulSoup
import requests
import csv


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
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
    field_names = ['nomer', 'kod_tovar', 'name', 'name2', 'name_original', 'brend', 'price', 'volume']
    csv_writer = csv.DictWriter(file, fieldnames=field_names)

    for page in range(1):  # 1, int(max_pages)
        response_page = requests.get(
            f'{link_catalog}page/{page}', headers=headers).text
        soup_page = BeautifulSoup(response_page, 'lxml')
        link_product = soup_page.select('.items > div > a')

        for link in link_product:
            url_href = link.get('href')
            response_tovar = requests.get(
                f'{link_site}{url_href}', headers=headers).text
            soup_link = BeautifulSoup(response_tovar, 'lxml')

            """ TODO: Name Catalog """
            name_catalog = soup_page.select_one('.page_layout>div>.list_title').text
            print(name_catalog)

            """ TODO: Name RU """
            name_tovar_span_ru = soup_link.select_one(
                '.item_layout>ul:first-child>li:nth-child(2)>div:last-child>span').text.replace('"', '')
            # print(name_tovar_span_ru)

            """ TODO: Name ENG"""
            name_tovar = soup_link.select_one(
                '.item_layout>ul:first-child>li:nth-child(2)>div:last-child')
            name_tovar.span.decompose()
            name_tovar_en = name_tovar.text
            print(name_tovar_en)

            """ TODO: PRICE """
            price = soup_link.find(itemprop="price").get('content')
            print(price)

            """ TODO: Razmer - Litrazh """
            # if soup_link.select_one('.price_block.volumes>li>a:first-child') is None:
            #     razmer = None
            # else:
            #     razmer = soup_link.select_one('.price_block.volumes>li>a:first-child')
            #     razmer.span.decompose()
            #     razmer = razmer.text
            #     print(razmer[8:])

            volume = soup_link.select_one('.price_block.volumes>li>a:first-child')
            if volume is None:
                volume = None
            else:
                volume.span.decompose()
                volume = volume.text[8:]
                print(volume[8:])

            """ TODO: Brend"""
            brend = soup_link.select_one('.crumbs>li:last-child>a>span').text
            print(brend)

            """ TODO: Name UA """
            response_tovar_ua = requests.get(
                f'{link_site_ua}{url_href}', headers=headers).text
            soup_link_ua = BeautifulSoup(response_tovar_ua, 'lxml')
            name_tovar_span_ua = soup_link_ua.select_one(
                '.item_layout>ul:first-child>li:nth-child(2)>div:last-child>span').text.replace('"', '')
            # print(name_tovar_span_ua)

            nomer += 1

            """ TODO: Kod Tovara """
            kod_tovar_1 = brend[:1].upper()
            kod_tovar_2 = brend[1:2].upper()
            kod_tovar_result = str(ord(kod_tovar_1)) + \
                '-' + str(ord(kod_tovar_2))
            kod_tovar = str(brend[:1].upper() + '-' +
                            price[:2] + '-' + kod_tovar_result + price[-2:])
            print(kod_tovar)

            csv_writer.writerow({
                'nomer': nomer,
                'kod_tovar': kod_tovar,
                'name': name_tovar_span_ru,
                'name2': name_tovar_span_ua,
                'name_original': name_tovar_en,
                'brend': brend,
                'price': price,
                'volume': volume
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
