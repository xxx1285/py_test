

from PIL import Image
from bs4 import BeautifulSoup
from transliterate import slugify
import requests
import csv
import os

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
link_site_ua = 'https://emm.ua/'
link_site_ru = 'ru/'
link_catalog = 'https://emm.ua/catalog/ortopedichni-matratsi/page-'
# link_catalog = 'https://emm.ua/catalog/mini-matratsi'

image_number = 0

nomer = 0

with open('emm_133.csv', 'w', newline='', encoding="utf-8") as file:
    field_names = ['name_tovar_ua', 'kod_tovar', 'brend', 'alias', 'price', 'matr_visot',
                   'matr_zhors', 'matr_nagruz', 'introtext_razm_price_vse', 'cont_name_harakt_vse',
                   'image', 'mimage1', 'mimage2', 'template'
                   ]
    csv_writer = csv.DictWriter(file, fieldnames=field_names, delimiter=';')
    csv_writer.writeheader()

    for page in range(1, 5):  # TODO:  number of page (страниц на 1 больше)
        response = requests.get(f'{link_catalog}{page}', headers=headers).text
        soup = BeautifulSoup(response, 'lxml')
        products_on_page = soup.select('.product-preview__name[href]')

        """ TODO: Name Catalog """
        # name_catalog = soup.select_one(
        #     '.page-heading.product-listing>span').text
        # print(name_catalog)

        """ TODO: Перебор каждого товара на странице"""
        for link in products_on_page:
            url_href = link_site_ua + link.get('href')

            response_tovar = requests.get(url_href, headers=headers).text
            soup_link = BeautifulSoup(response_tovar, 'lxml')

            """ TODO: Name UA """
            name_tovar_ua = soup_link.select_one('.product__heading span').text
            print(name_tovar_ua)

            """ TODO: PRICE """
            # price = soup_link.find(name="twitter:label1").get('content')
            price = soup_link.find("meta", {"name": "twitter:label1"}).attrs['content']
            price = price[:-4]
            # print(price)

            """ TODO: Brend  """
            brend = soup_link.find('spanitemprop').text

            """ TODO:  Matras Visota  """
            matr_visot = soup_link.select_one(
                '.product__main-features .product__m-feature-item:nth-child(1)\
                    .product__m-feature-value span')
            matr_visot = '0' if matr_visot is None else matr_visot.get_text()


            """ TODO:  Zhorstkost and Nagruzka matras  """
            del_zhor_1 = soup_link.select_one('.product__main-features\
                .product__m-feature-item:nth-child(2) .product__m-feature-icon img')
            del_zhor_1 = '0' if del_zhor_1 is None else del_zhor_1.attrs['src']
            # print(del_zhor_1)

            del_zhor_2 = soup_link.select_one('.product__main-features\
                .product__m-feature-item:nth-child(3) .product__m-feature-icon img')
            del_zhor_2 = '0' if del_zhor_2 is None else del_zhor_2.attrs['src']

            if del_zhor_1 == 'https://emm.ua/files/features/feauture-icon-1.svg':
                matr_zhors = soup_link.select_one('.product__main-features\
                .product__m-feature-item:nth-child(2) .product__m-feature-desc\
                    .product__m-feature-value span').get_text()
            elif del_zhor_1 == 'https://emm.ua/files/features/feauture-icon-3.svg':
                matr_nagruz = soup_link.select_one('.product__main-features\
                .product__m-feature-item:nth-child(2) .product__m-feature-desc\
                    .product__m-feature-value span').get_text()
            else:
                matr_zhors = '0'

            if del_zhor_2 == 'https://emm.ua/files/features/feauture-icon-3.svg':
                matr_nagruz = soup_link.select_one('.product__main-features\
                .product__m-feature-item:nth-child(3) .product__m-feature-desc\
                    .product__m-feature-value span').get_text()
            else:
                matr_nagruz = '0'

            """ TODO:  Introtext - Razmer and Price  """
            introtext_soup_razm_price = soup_link.select('.product__size-select .js_select2 option')

            intro_price_razmer = []

            for intro in introtext_soup_razm_price:
                intro_price = intro.get('data-price')
                intro_razmer = intro.get_text()
                intro_price_razmer.append(f'<tr><th scope="row">{intro_razmer}</th><td>{intro_price} грн.</td></tr>')

            introtext_razm_price_vse = ''.join(intro_price_razmer)

            """ TODO:  Content - Harakteristik  """
            content_harakterist_vse = soup_link.select('ul .product__feature-item')

            cont_name_harakt = []

            for cont in content_harakterist_vse:
                cont_name = cont.select_one('.product__feature-name span').get_text()
                cont_harakt = cont.select_one('.product__feature-value').get_text()
                cont_name_harakt.append(f'<tr><th scope="row">{cont_name}</th><td>{cont_harakt}</td></tr>')

            cont_name_harakt_vse = ''.join(cont_name_harakt)

            """ TODO: Kod Tovara """
            kod_tovar_1 = brend[:1].upper()
            kod_tovar_2 = name_tovar_ua[-6:-5].upper()
            kod_tovar_3 = name_tovar_ua[-5:-4].upper()
            kod_tovar_4 = name_tovar_ua[-3:-2].upper()
            kod_tovar_result = str(ord(kod_tovar_4)) + \
                '-' + str(ord(kod_tovar_2)) + '-' + str(ord(kod_tovar_3))
            kod_tovar = str(brend[:1].upper() + '-' + kod_tovar_result)
            print(kod_tovar)

            """ TODO: Number """
            nomer += 1

            """ TODO: IMAGES """
            one_images_href = soup_link.select_one('.product__gallery\
                .product__images-slide a').get('href')
            image_content = requests.get(one_images_href, headers=headers).content

            """ TODO: name image """
            translit_name = slugify(name_tovar_ua)
            translit_name2 = slugify(name_tovar_ua + ' матрас')

            translit_name = translit_name2 if translit_name is None else translit_name

            transliter_name_image = translit_name + \
                '-kiev-odesa-lviv-' + str(image_number)
            alias = translit_name + '-kiev-borispol-brovary-matras'
            image_number += 1

            """ TODO: create folders """
            work_dir = os.getcwd() + r"\images\EMM\ortopedichni-matratsi"
            path_images = os.path.join(work_dir, translit_name)
            ''' TODO: if folders not, create new folders'''
            if not os.path.exists(path_images):
                os.mkdir(path_images)

            """ TODO: verification JPG and save on disk"""
            _, ext = os.path.splitext(one_images_href)

            if ext in (".jpg"):
                with open(f'{path_images}/{transliter_name_image}.jpg', 'wb') as file:
                    file.write(image_content)
            elif ext in (".png"):
                with open(f'{path_images}/{transliter_name_image}.png', 'wb') as file:
                    file.write(image_content)

                    im = Image.open(f'{path_images}/{transliter_name_image}.png')

                    fill_color = (225, 225, 225)  # your new background color

                    im = im.convert("RGBA")   # it had mode P after DL it from OP
                    if im.mode in ('RGBA', 'LA'):
                        background = Image.new(im.mode[:-1], im.size, fill_color)
                        background.paste(im, im.split()[-1])  # omit transparency
                        im = background

                    im.convert("RGB").save(f'{path_images}/{transliter_name_image}.jpg')

                    image_adress = (f'images/EMM/ortopedichni-matratsi/{translit_name}/{transliter_name_image}.jpg')

                    # close file - free memory
                    file.close()

                    # del png
                    os.remove(f'{path_images}/{transliter_name_image}.png')
            else:
                print('Error ' + ext)
                None

            img0 = image_adress
            img1 = (f'images/EMM/ortopedichni-matratsi/img1-EMM.jpg')
            img2 = (f'images/EMM/ortopedichni-matratsi/img2-EMM.jpg')

            ''' TODO: Template'''
            template = 16

            """ TODO: CSV Write """

            csv_writer.writerow({
                'name_tovar_ua': name_tovar_ua,
                'kod_tovar': kod_tovar,
                'template': template,
                # 'name_catalog': name_catalog,
                'brend': brend,
                'alias': alias,
                'price': price,
                'matr_visot': matr_visot,
                'matr_zhors': matr_zhors,
                'matr_nagruz': matr_nagruz,
                'introtext_razm_price_vse': introtext_razm_price_vse,
                'cont_name_harakt_vse': cont_name_harakt_vse,
                'image': img0,
                'mimage1': img1,
                'mimage2': img2
            })
