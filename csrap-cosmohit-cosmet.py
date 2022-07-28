

from bs4 import BeautifulSoup
from transliterate import slugify
import requests
import csv
import os

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
link_site_ua = 'https://constanta.ua/'
link_site_ru = 'ru/'
link_catalog = 'https://cosmohit.ua/catalogue/cosmetics/page/'

image_number = 0

nomer = 0

with open('129.csv', 'w', newline='', encoding="utf-8") as file:
    field_names = ['name_tovar_ua', 'kod_tovar', 'brend', 'price', 'image'
                   ]
    csv_writer = csv.DictWriter(file, fieldnames=field_names, delimiter=';')
    csv_writer.writeheader()
    for page in range(1, 833):  # TODO:  number of page (страниц на 1 больше)
        print(page)
        response = requests.get(f'{link_catalog}{page}', headers=headers).text
        soup = BeautifulSoup(response, 'lxml')
        products_on_page = soup.select('.items > div > a')

        """ TODO: Name Catalog """
        # name_catalog = soup.select_one(
        #     '.page-heading.product-listing>span').text
        # print(name_catalog)

        """ TODO: Перебор каждого товара на странице"""
        for link in products_on_page:
            url_href = link.get('href')
            response_tovar = requests.get(url_href, headers=headers).text
            soup_link = BeautifulSoup(response_tovar, 'lxml')

            """ TODO: Name UA """
            name_tovar_ua = soup_link.select_one('.pb-right-column h1').text
            # print(name_tovar_ua)

            """ TODO: PRICE """
            price = soup_link.find(
                property="product:price:amount").get('content')

            """ TODO: Brend  """
            brend = soup_link.select_one(
                '.table-data-sheet tr:nth-child(1) td:nth-child(2)')
            brend = '0' if brend is None else brend.get_text()

            """ TODO:  Dlinna  """
            dlina = soup_link.select_one(
                '.product-information .tab-content #product-description-tab-content\
                    .rte .product-ico:nth-child(4) div:nth-child(1) span')
            dlina = '0' if dlina is None else dlina.get_text()

            """ TODO:  Glubina  """
            glubina = soup_link.select_one(
                '.product-information .tab-content #product-description-tab-content\
                    .rte .product-ico:nth-child(4) div:nth-child(2) span')
            glubina = '0' if glubina is None else glubina.get_text()

            """ TODO:  Visota  """
            visota = soup_link.select_one(
                '.product-information .tab-content #product-description-tab-content\
                    .rte .product-ico:nth-child(4) div:nth-child(3) span')
            visota = '0' if visota is None else visota.get_text()

            """ TODO: Spalnoe Mesto  """
            spalnoe = soup_link.select_one(
                '.product-information .tab-content #product-description-tab-content\
                    .rte .product-ico:nth-child(4) div:nth-child(4) span')
            if spalnoe is None:
                spalnoe = '0'
            else:
                spalnoe = spalnoe.get_text()

            """ TODO: Kod Tovara """
            kod_tovar_1 = brend[:1].upper()
            kod_tovar_2 = brend[1:2].upper()
            kod_tovar_result = str(ord(kod_tovar_1)) + \
                '-' + str(ord(kod_tovar_2))
            kod_tovar = str(brend[:1].upper() + '-' +
                            price[:2] + '-' + kod_tovar_result + price[-2:])

            """ TODO: Number """
            nomer += 1

            """ TODO: IMAGES """

            all_images = soup_link.select(
                '#thumbs_list #thumbs_list_frame li a')

            all_images_name = []

            for images in all_images:
                image_url = images.get('href')
                image_content = requests.get(image_url).content

                translit_name = slugify(name_tovar_ua)
                translit_name2 = slugify(name_tovar_ua + ' диван')

                translit_name = translit_name2 if translit_name is None else translit_name

                transliter_name_image = translit_name + \
                    '-kiev-odesa-lviv-' + str(image_number)
                image_number += 1

                """ TODO: create folders """
                work_dir = os.getcwd() + r"\images\konstanta\lizhka"
                path_images = os.path.join(work_dir, translit_name)
                ''' TODO: if folders not, create new folders'''
                if not os.path.exists(path_images):
                    os.mkdir(path_images)

                """ TODO: verification JPG and save on disk"""
                _, ext = os.path.splitext(image_url)
                if ext in (".jpg"):
                    with open(f'{path_images}/{transliter_name_image}.jpg', 'wb') as file:
                        file.write(image_content)
                else:
                    print('Error ' + ext)
                    None

                all_images_name.append(
                    f'images/konstanta-site/{translit_name}/{transliter_name_image}.jpg')

            """ TODO: images to img1, img2, img3,... """

            len_all_images_name = len(all_images_name)

            img0 = all_images_name[0]

            csv_writer.writerow({
                'name_tovar_ua': name_tovar_ua,
                'kod_tovar': kod_tovar,
                # 'name_catalog': name_catalog,
                'brend': brend,
                'price': price,
                'image': img0
            })
