from bs4 import BeautifulSoup
import re
from slugify import slugify
import requests
import csv
import os

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
link_site_ua = 'https://mixmebli.com/catalogs'

image_number = 0
nomer = 0

# CATALOG
response = requests.get(link_site_ua, headers=headers).text
soup = BeautifulSoup(response, 'lxml')
all_category_in_catalog = soup.select(".category-wall .caption a")

with open('1334.csv', 'w', newline='', encoding="utf-8") as file:
    field_names = ['pagetitle', 'description', 'alias', 'articul', 'brend', 'price', 'proizvod',
                    'image', 'mimage1', 'mimage2', 'mimage3', 'mimage4', 'mimage5',
                    'mimage6', 'mimage7', 'mimage8', 'mimage9', 'mimage10', 'mimage11',
                    'color', 'zag_razmer', 'content']
    csv_writer = csv.DictWriter(file, fieldnames=field_names, delimiter=';')
    csv_writer.writeheader()

    # CATEGORY CATALOG
    for category in all_category_in_catalog:
        url_category = category.get('href')

        requests_category = requests.get(url_category, headers=headers).text
        soup_category = BeautifulSoup(requests_category, 'lxml')

        # NOMERA STRANITS CATEGORY
        all_num_pages_category = soup_category.select_one(".pagination > li:last-child > a")
        if all_num_pages_category is None:
            all_num_pages_category = 2 # Range 1+1
        else:
            all_num_pages_category = all_num_pages_category.get('href')
            all_num_pages_category = int(all_num_pages_category[all_num_pages_category.find("=") + 1:]) + 1
        """ Name Catalog """
        name_catalog = soup_category.select_one('.category-title').text

        """ alias Catalog """
        replacements_symbols = [['Ü', 'UE'], ['ü', 'ue'], ['і', 'i'],
            ['І', 'I'], ['ї', 'i'], ['є', 'e'], ['є', 'e'], ["'", '']]
        alias_catalog = slugify(name_catalog.lower(), replacements=replacements_symbols)

        for page in range(1, all_num_pages_category):  # TODO:  number of page (страниц на 1 больше)

            response_page_category = requests.get(f'{url_category}?page={page})', headers=headers).text
            soup_page_category = BeautifulSoup(response_page_category, 'lxml')
            # print(f'{url_category}?page={page}')

            products_on_page = soup_page_category.select('.product-block .name a[href]')

            """ Перебор каждого товара на странице"""
            for link_tovar in products_on_page:
                url_href = link_tovar.get('href')
                response_tovar = requests.get(url_href, headers=headers).text
                soup_tovar = BeautifulSoup(response_tovar, 'lxml')

                """ Name UA """
                pagetitle = soup_tovar.select_one('.page-product .title-product').text
                print(pagetitle)

                """ Name Colections """
                description = name_catalog

                """ PRICE """
                # price = soup_tovar.find(property="product:price:amount").get('content')
                price = 0

                """ Brend + Kraina  """
                brend = 'MX'
                proizvod = 'Україна'

                """ Rozmir  """
                zag_razmer = soup_tovar.select_one('#tab-description p:nth-child(1)').text
                zag_razmer = zag_razmer[8:]

                """ Content  """
                content = soup_tovar.select_one('#tab-description')

                """ Color  """
                if soup_tovar.find("b", string=re.compile("Колір:")):
                    color_tovar = soup_tovar.find("b", string=re.compile("Колір:")).next_sibling.text
                elif soup_tovar.find("b", string=re.compile("Цвет:")):
                    color_tovar = soup_tovar.find("b", string=re.compile("Цвет:")).next_sibling.text
                elif soup_tovar.find("strong", string=re.compile("Колір:")):
                    color_tovar = soup_tovar.find("strong", string=re.compile("Колір:")).next_sibling.text
                else:
                    color_tovar = 0

                # # dlina = soup_tovar.select_one(
                # #     '.product-information .tab-content #product-description-tab-content\
                # #         .rte .product-ico:nth-child(4) div:nth-child(1) span')
                # dlina = soup_tovar.select_one('img[src="/img/ico/shirina.png"]').next_sibling
                # # dlina2 = soup_tovar.find(attrs={'src': '/img/ico/shirina.png'}).next_element
                # dlina = '0' if dlina is None else dlina.get_text()

                # """ TODO:  Glubina  """
                # glubina = soup_tovar.select_one('img[src="/img/ico/glubina.png"]')
                # print(glubina)
                # glubina = '0' if glubina is None else glubina.next_sibling.get_text()
                # print(glubina)

                # """ TODO:  Visota  """
                # visota = soup_tovar.select_one('img[src="/img/ico/vysota.png"]')
                # visota = '0' if visota is None else visota.next_sibling.get_text()

                # """ TODO: Spalnoe Mesto  """
                # spalnoe = soup_tovar.select_one('img[src="/img/ico/spalnoe-mesto.png"]')
                # if spalnoe is None:
                #     spalnoe = '0'
                # else:
                #     spalnoe = spalnoe.next_sibling.get_text()

                """ TODO: Articul """
                kod_tovar_1 = url_href[-1:].upper()
                kod_tovar_2 = url_href[-6:-5].upper()
                kod_tovar_3 = url_href[-10:-9]
                kod_tovar_4 = url_href[-16:-15]
                kod_tovar_result = str(ord(kod_tovar_1)) + \
                    '-' + str(ord(kod_tovar_2)) + str(ord(kod_tovar_3)) + str(ord(kod_tovar_4))

                articul = str('MX' + kod_tovar_result)

                """ TODO: ALIAS """
                alias_tovar = slugify(pagetitle.lower(), replacements=replacements_symbols)

                """ TODO: Number """
                nomer += 1

                """ TODO: IMAGES IMAGESIMAGES """

                all_images = soup_tovar.select('.product-info img')
                all_images_name = []

                for images in all_images:
                    # image_url = images.get('data-zoom-image')
                    if images.get('data-zoom-image'):
                        image_url = images.get('data-zoom-image')
                    else:
                        image_url = images.get('src')

                    image_content = requests.get(image_url, headers=headers).content

                    """ transliterats images """

                    translit_name = slugify(pagetitle.lower(), replacements=replacements_symbols)
                    translit_name2 = slugify(pagetitle + ' МХ меблі Киев')
                    translit_name = translit_name2 if translit_name is None else translit_name

                    transliter_name_image = translit_name + \
                        '-kiev-vinnitsya-kovel-lviv-borispol-ternopil' + str(image_number)
                    image_number += 1

                    """ TODO: create folders """
                    work_dir = os.getcwd() + r"\images\mix-mebel"
                    path_images = os.path.join(work_dir, alias_catalog, translit_name)
                    ''' TODO: if folders not, create new folders'''
                    if not os.path.exists(path_images):
                        # os.mkdir(path_images)
                        os.makedirs(path_images)

                    """ TODO: verification JPG and save on disk"""
                    _, ext = os.path.splitext(image_url)

                    # if ext in (".jpg"):
                    if ext in [".jpg", ".JPG"]:
                        with open(f'{path_images}/{transliter_name_image}.jpg', 'wb') as file:
                            file.write(image_content)
                    else:
                        print(pagetitle + 'Error ' + ext)
                        None

                    all_images_name.append(
                        f'images/mix-mebel/{alias_catalog}/{translit_name}/{transliter_name_image}.jpg')

                """ TODO: images to img1, img2, img3,... """

                len_all_images_name = len(all_images_name)

                img0 = all_images_name[0]

                img = 0

                if 1 < len_all_images_name:
                    img1 = all_images_name[1]
                else:
                    img1 = '0'
                if 2 < len_all_images_name:
                    img2 = all_images_name[2]
                else:
                    img2 = '0'
                if 3 < len_all_images_name:
                    img3 = all_images_name[3]
                else:
                    img3 = '0'
                if 4 < len_all_images_name:
                    img4 = all_images_name[4]
                else:
                    img4 = '0'
                if 5 < len_all_images_name:
                    img5 = all_images_name[5]
                else:
                    img5 = '0'
                if 6 < len_all_images_name:
                    img6 = all_images_name[6]
                else:
                    img6 = '0'
                if 7 < len_all_images_name:
                    img7 = all_images_name[7]
                else:
                    img7 = '0'
                if 8 < len_all_images_name:
                    img8 = all_images_name[8]
                else:
                    img8 = '0'
                if 9 < len_all_images_name:
                    img9 = all_images_name[9]
                else:
                    img9 = '0'
                if 10 < len_all_images_name:
                    img10 = all_images_name[10]
                else:
                    img10 = '0'
                if 11 < len_all_images_name:
                    img11 = all_images_name[11]
                else:
                    img11 = '0'
                # if 12 < len_all_images_name:
                #     img12 = all_images_name[12]
                # else:
                #     img12 = '0'
                # if 13 < len_all_images_name:
                #     img13 = all_images_name[13]
                # else:
                #     img13 = '0'
                # if 14 < len_all_images_name:
                #     img14 = all_images_name[14]
                # else:
                #     img14 = '0'
                # if 15 < len_all_images_name:
                #     img15 = all_images_name[15]
                # else:
                #     img15 = '0'
                # if 16 < len_all_images_name:
                #     img16 = all_images_name[16]
                # else:
                #     img16 = '0'
                # if 17 < len_all_images_name:
                #     img17 = all_images_name[17]
                # else:
                #     img17 = '0'
                # if 18 < len_all_images_name:
                #     img18 = all_images_name[18]
                # else:
                #     img18 = '0'
                # if 19 < len_all_images_name:
                #     img19 = all_images_name[19]
                # else:
                #     img19 = '0'
                # if 20 < len_all_images_name:
                #     img20 = all_images_name[20]
                # else:
                #     img20 = '0'

                csv_writer.writerow({
                    'pagetitle': pagetitle,
                    'description': description,
                    'articul': articul,
                    'brend': brend,
                    'proizvod': proizvod,
                    'price': price,
                    'zag_razmer': zag_razmer,
                    'content': content,
                    'color': color_tovar,
                    'alias': alias_tovar,
                    'image': img0,
                    'mimage1': img1,
                    'mimage2': img2,
                    'mimage3': img3,
                    'mimage4': img4,
                    'mimage5': img5,
                    'mimage6': img6,
                    'mimage7': img7,
                    'mimage8': img8,
                    'mimage9': img9,
                    'mimage10': img10,
                    'mimage11': img11
                    # 'mimage12': img12,
                    # 'mimage13': img13,
                    # 'mimage14': img14,
                    # 'mimage15': img15,
                    # 'mimage16': img16,
                    # 'mimage17': img17,
                    # 'mimage18': img18,
                    # 'mimage19': img19,
                    # 'mimage20': img20
                })
