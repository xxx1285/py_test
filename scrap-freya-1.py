

from bs4 import BeautifulSoup
import requests
import csv


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
image_number = 0
page_number = 1
link_site = 'https://constanta.ua/ru/'
link_site_ua = 'https://constanta.ua/'
link_catalog = 'https://constanta.ua/80-divany?id_category=80&n=124'

response = requests.get(link_catalog, headers=headers).text
soup = BeautifulSoup(response, 'lxml')
# max_pages = soup.select_one('.paginator > a:nth-child(5)').get_text()
nomer = 0

with open('112.csv', 'w', encoding='utf-8') as file:
    field_names = ['nomer', 'kod_tovar', 'name', 'name2', 'name_original', 'brend', 'price', 'volume']
    csv_writer = csv.DictWriter(file, fieldnames=field_names)

    # for page in range(1):  # 1, int(max_pages)
    #     response_page = requests.get(
    #         f'{link_catalog}page/{page}', headers=headers).text
    #     soup_page = BeautifulSoup(response_page, 'lxml')
    link_product = soup.select('ul.product_list.grid > li .product-container h5 a')

    for link in link_product:
        url_href = link.get('href')
        url_href2 = 'https://constanta.ua/pryami-divani/63-madrid.html'
        response_tovar = requests.get(url_href2, headers=headers).text
        soup_link = BeautifulSoup(response_tovar, 'lxml')

        """ TODO: Name Catalog """
        name_catalog = soup.select_one('.page-heading.product-listing>span')

        """ TODO: Name UA """
        name_tovar_ua = soup_link.select_one('.pb-right-column h1').text
        print(name_tovar_ua)

        """ TODO: PRICE """
        price = soup_link.find(property="product:price:amount").get('content')
        print(price)

        """ TODO: Brend  """
        brend = soup_link.select_one('.table-data-sheet tr:nth-child(1) td:nth-child(2)').text
        print(brend)

        """ TODO:  Dlinna  """
        dlina = soup_link.select_one('.product-information .tab-content #product-description-tab-content .rte .product-ico:nth-child(4) div:nth-child(1) span')
        dlina = '0' if dlina is None else dlina.get_text()
        # if dlina is None:
        #     dlina = '0'
        # else:
        #     dlina.get_text()
        print(dlina)

        # """ TODO:  Glubina  """
        # glubina = soup_link.select_one('.product-information .tab-content #product-description-tab-content .rte .product-ico:nth-child(4) div:nth-child(2) span').text

        # """ TODO:  Visota  """
        # visota = soup_link.select_one('.product-information .tab-content #product-description-tab-content .rte .product-ico:nth-child(4) div:nth-child(3) span').text

        # """ TODO: Spalnoe Mesto  """
        # spalnoe = soup_link.select_one('.product-information .tab-content #product-description-tab-content .rte .product-ico:nth-child(4) div:nth-child(4) span')
        # if spalnoe is None:
        #     spalnoe = '0'
        # else:
        #     spalnoe = spalnoe.get_text()
        # print(brend + dlina + glubina + visota + spalnoe)

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
            'name': name_tovar_ua,
            'name2': name_tovar_span_ua,
            'name_original': name_tovar_en,
            'brend': brend,
            'price': price,
            'volume': volume
        })
