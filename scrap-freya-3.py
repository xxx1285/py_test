

from bs4 import BeautifulSoup
import requests
import csv

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
link_site_ua = 'https://constanta.ua/'
link_site_ru = 'ru/'
link_catalog = 'https://constanta.ua/80-divani?p='

image_number = 0

# response = requests.get(f'{link_catalog}', headers=headers).text
# soup = BeautifulSoup(response, 'lxml')
# max_pages = soup.select_one('.paginator > a:nth-child(5)').get_text()
nomer = 0

with open('113.csv', 'w', encoding='utf-8') as file:
    field_names = ['nomer', 'kod_tovar', 'name_catalog', 'brend', 'name_tovar_ua', 'price', 'dlina', 'glubina', 'visota', 'spalnoe']
    csv_writer = csv.DictWriter(file, fieldnames=field_names)
    for page in range(1, 10):  # TODO:  number of page (страниц на 1 больше)
        response = requests.get(f'{link_catalog}{page})', headers=headers).text
        print(page)
        soup = BeautifulSoup(response, 'lxml')
        products_on_page = soup.select('ul.product_list.grid > li .product-container h5 a[href]')

        """ TODO: Name Catalog """
        name_catalog = soup.select_one('.page-heading.product-listing>span').text
        # print(name_catalog)

        for link in products_on_page:
            url_href = link.get('href')
            response_tovar = requests.get(url_href, headers=headers).text
            soup_link = BeautifulSoup(response_tovar, 'lxml')

            """ TODO: Name UA """
            name_tovar_ua = soup_link.select_one('.pb-right-column h1').text
            # print(name_tovar_ua)

            """ TODO: PRICE """
            price = soup_link.find(property="product:price:amount").get('content')

            """ TODO: Brend  """
            brend = soup_link.select_one('.table-data-sheet tr:nth-child(1) td:nth-child(2)')
            brend = '0' if brend is None else brend.get_text()

            """ TODO:  Dlinna  """
            dlina = soup_link.select_one('.product-information .tab-content #product-description-tab-content .rte .product-ico:nth-child(4) div:nth-child(1) span')
            dlina = '0' if dlina is None else dlina.get_text()

            """ TODO:  Glubina  """
            glubina = soup_link.select_one('.product-information .tab-content #product-description-tab-content .rte .product-ico:nth-child(4) div:nth-child(2) span')
            glubina = '0' if glubina is None else glubina.get_text()

            """ TODO:  Visota  """
            visota = soup_link.select_one('.product-information .tab-content #product-description-tab-content .rte .product-ico:nth-child(4) div:nth-child(3) span')
            visota = '0' if visota is None else visota.get_text()

            """ TODO: Spalnoe Mesto  """
            spalnoe = soup_link.select_one('.product-information .tab-content #product-description-tab-content .rte .product-ico:nth-child(4) div:nth-child(4) span')
            if spalnoe is None:
                spalnoe = '0'
            else:
                spalnoe = spalnoe.get_text()
            print(brend + name_tovar_ua + dlina + glubina + visota + spalnoe)

            """ TODO: Kod Tovara """
            kod_tovar_1 = brend[:1].upper()
            kod_tovar_2 = brend[1:2].upper()
            kod_tovar_result = str(ord(kod_tovar_1)) + \
                '-' + str(ord(kod_tovar_2))
            kod_tovar = str(brend[:1].upper() + '-' +
                            price[:2] + '-' + kod_tovar_result + price[-2:])
            print(kod_tovar)

            """ TODO: Number """
            nomer += 1


            csv_writer.writerow({
                'nomer': nomer,
                'kod_tovar': kod_tovar,
                'name_catalog': name_catalog,
                'brend': brend,
                'name_tovar_ua': name_tovar_ua,
                'price': price,
                'dlina': dlina,
                'glubina': glubina,
                'visota': visota,
                'spalnoe': spalnoe
            })
