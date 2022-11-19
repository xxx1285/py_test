

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
link_site_ua = 'https://www.bis-m.ua'
# link_site_ru = 'ru/'
link_catalog = 'https://www.bis-m.ua/ua/myagkaya-mebel-bis-m'

nomer = 0

with open('bis-m-1.csv', 'w', newline='', encoding="utf-8") as file:
    field_names = ['name_tovar_ua', 'articul', 'articul_url', 'brend',
                   'price', 'cont_name_harakt','image', 'mimage1',
                   'mimage2', 'mimage3', 'mimage4', 'mimage5', 'mimage6',
                   'mimage7', 'mimage8', 'mimage9', 'mimage10', 'mimage11',
                   'mimage12', 'mimage13', 'mimage14', 'mimage15',
                   'mimage16', 'mimage17', 'mimage18', 'mimage19', 'mimage20',
                   'image_har_1', 'image_har_2', 'image_har_3', 'image_har_4',
                   'image_har_5', 'image_har_6'
                    ]
    csv_writer = csv.DictWriter(file, fieldnames=field_names, delimiter=';')
    csv_writer.writeheader()

    """Прохід по розділам в каталог: дивани, крісла ...."""
    response_0 = requests.get(link_catalog, headers=headers).text
    soup_0 = BeautifulSoup(response_0, 'lxml')
    category_in_catalog = soup_0.select('.categoryimage > a[href]')

    for link in category_in_catalog:
        url_href = link.get('href')

        """Прохід по каталогу з вибором HREF товарів"""
        response_1 = requests.get(f'{link_site_ua}{url_href})', headers=headers).text
        soup_1 = BeautifulSoup(response_1, 'lxml')
        products_in_category = soup_1.select('.supcatitem-title > a[href]')

        """ Перебираємо кожний товар """
        for link in products_in_category:
            product_href = link.get('href')
            response_product = requests.get(f'{link_site_ua}{product_href})', headers=headers).text
            soup_link = BeautifulSoup(response_product, 'lxml')

            """ * Беремо унікальний урл товару що слугуватиме його кодом"""
            articul_url = (''.join(product_href.split('/')[-1]))

            """ TODO: Name UA """
            name_tovar_ua = soup_link.select_one('#comjshop h1').get_text()
            print(name_tovar_ua)

            """ TODO: PRICE """
            # price = soup_link.select_one('.productfull #block_price').text
            price = soup_link.find("div", {"property": "schema:price"}).attrs['content']

            """ TODO: Brend  """
            brend = 'BM'

            """ TODO: Kod Tovara """
            # <input name="product_id" id="product_id" value="1552">
            kod_prod_1 = soup_link.find("input", {"name": "product_id"}).attrs['value']
            # <input name="category_id" id="category_id" value="3">
            kod_prod_2 = soup_link.find("input", {"name": "category_id"}).attrs['value']
            kod_prod_3 = str(ord(name_tovar_ua[:1].upper()))
            articul = str(kod_prod_1 + '-' + kod_prod_2 + '-' + kod_prod_3)

            """ TODO: Number """
            nomer += 1

            """ TODO:  Content - Harakteristik  """
            content_harakterist_vse = soup_link.select('.extra_fields_el')
            cont_name_harakt = []

            for cont in content_harakterist_vse:
                cont_name = cont.select_one('.extra_fields_name').get_text()
                cont_harakt = cont.select_one('.extra_fields_value').get_text()
                cont_name_harakt.append(f'<p class="text-start"><span class="fw-bold">{cont_name}</span>\
                    <span class="text-decoration-underline">{cont_harakt}</span></p>')
            cont_name_harakt = ''.join(cont_name_harakt)  # convert list[] in str

            """ TODO: IMAGES """
            all_images = soup_link.select('#list_product_image_middle img')
            all_images_name = []
            image_number = 0
            for images in all_images:
                if not (images.get('src') is None):
                    image_url = images.get('src')
                    image_content = requests.get(image_url).content

                    translit_name = slugify(name_tovar_ua)
                    translit_name2 = slugify(name_tovar_ua + ' диван')

                    translit_name = translit_name2 if translit_name is None else translit_name

                    transliter_name_image = translit_name + \
                        '-kiev-odesa-vinnitsya-boryspil-' + str(image_number)
                    image_number += 1

                    """ TODO: create folders """
                    work_dir = os.getcwd() + r"\images\BisM-scrp"  # робоча директория
                    path_images = os.path.join(work_dir, translit_name)

                    ''' Створюємо папку якщо відсутня'''
                    if not os.path.exists(path_images):
                        os.mkdir(path_images)

                    """ перевіряємо розширення _ це назва, ехт - це розширення """
                    _, ext = os.path.splitext(image_url)  # ext - берем розширення

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
                            # image_adress = (f'images/BisM-parce/{translit_name}/{transliter_name_image}.jpg')
                            file.close()  # close file - free memory
                            # del png
                            os.remove(f'{path_images}/{transliter_name_image}.png')
                    else:
                        print('Error ' + ext)
                        None

                    all_images_name.append(
                        f'images/BisM-scrp/{translit_name}/{transliter_name_image}.jpg')

            """ TODO: IMG BIG"""
            # img_big = soup_link.select_one('.ls-wrapper')

            """ TODO: DOP Harakteristik IMAGES """
            all_images_harakreristik = soup_link.select('.jshop_prod_description img')
            all_images_harakter_list = []
            if not (all_images_harakreristik is None):
                for images in all_images_harakreristik:
                    if not (images.get('src') is None):
                        image_url = images.get('src')
                        image_content = requests.get(f'{link_site_ua}{image_url}').content

                        translit_name = slugify(name_tovar_ua)
                        translit_name2 = slugify(name_tovar_ua + ' диван')
                        translit_name = translit_name2 if translit_name is None else translit_name
                        transliter_name_image = translit_name + \
                            '-kiev-lviv-kamyanets-podolsk-' + str(image_number)
                        image_number += 1

                        """ TODO: create folders """
                        work_dir = os.getcwd() + r"\images\BisM-scrp" # робоча директория
                        path_images = os.path.join(work_dir, translit_name)

                        ''' Створюємо папку якщо відсутня'''
                        if not os.path.exists(path_images):
                            os.mkdir(path_images)

                        """ перевіряємо розширення _ це назва, ехт - це розширення"""
                        _, ext = os.path.splitext(image_url)  # ext - берем розширення

                        if ext in (".jpg"):
                            with open(f'{path_images}/{transliter_name_image}.jpg', 'wb') as file:
                                file.write(image_content)
                        elif ext in (".webp"):
                            with open(f'{path_images}/{transliter_name_image}.webp', 'wb') as file:
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
                                # image_adress = (f'images/BisM-parce/{translit_name}/{transliter_name_image}.jpg')
                                file.close()  # close file - free memory
                                # del png
                                os.remove(f'{path_images}/{transliter_name_image}.png')
                        else:
                            print('Error ' + ext)
                            None

                        all_images_harakter_list.append(
                            f'images/BisM-scrp/{translit_name}/{transliter_name_image}.jpg')

            """ TODO: images to img1, img2, img3,... """
            len_all_images_name = len(all_images_name)
            img0 = all_images_name[0]

            # for i in range(1, 21):  # TODO:  num of page (стр на 1 больше)
            #     if i < len_all_images_name:
            #         img[i] = all_images_name[i]
            #         print(img[i])
            #     else:
            #         img1 = '0'

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
            if 12 < len_all_images_name:
                img12 = all_images_name[12]
            else:
                img12 = '0'
            if 13 < len_all_images_name:
                img13 = all_images_name[13]
            else:
                img13 = '0'
            if 14 < len_all_images_name:
                img14 = all_images_name[14]
            else:
                img14 = '0'
            if 15 < len_all_images_name:
                img15 = all_images_name[15]
            else:
                img15 = '0'
            if 16 < len_all_images_name:
                img16 = all_images_name[16]
            else:
                img16 = '0'
            if 17 < len_all_images_name:
                img17 = all_images_name[17]
            else:
                img17 = '0'
            if 18 < len_all_images_name:
                img18 = all_images_name[18]
            else:
                img18 = '0'
            if 19 < len_all_images_name:
                img19 = all_images_name[19]
            else:
                img19 = '0'
            if 20 < len_all_images_name:
                img20 = all_images_name[20]
            else:
                img20 = '0'

            """ TODO: All images haracteristik list """
            len_all_images_harakteriskik = len(all_images_harakter_list)

            if len_all_images_harakteriskik >= 1:
                imghar1 = all_images_harakter_list[0]
            else:
                imghar1 = '0'
            if len_all_images_harakteriskik >= 2:
                imghar2 = all_images_harakter_list[1]
            else:
                imghar2 = '0'
            if len_all_images_harakteriskik >= 3:
                imghar3 = all_images_harakter_list[2]
            else:
                imghar3 = '0'
            if len_all_images_harakteriskik >= 4:
                imghar4 = all_images_harakter_list[3]
            else:
                imghar4 = '0'
            if len_all_images_harakteriskik >= 5:
                imghar5 = all_images_harakter_list[4]
            else:
                imghar5 = '0'
            if len_all_images_harakteriskik >= 6:
                imghar6 = all_images_harakter_list[5]
            else:
                imghar6 = '0'

            csv_writer.writerow({
                'name_tovar_ua': name_tovar_ua,
                'articul': articul,
                'articul_url': articul_url,
                'brend': brend,
                'price': price,
                'cont_name_harakt': cont_name_harakt,
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
                'mimage11': img11,
                'mimage12': img12,
                'mimage13': img13,
                'mimage14': img14,
                'mimage15': img15,
                'mimage16': img16,
                'mimage17': img17,
                'mimage18': img18,
                'mimage19': img19,
                'mimage20': img20,
                'image_har_1': imghar1,
                'image_har_2': imghar2,
                'image_har_3': imghar3,
                'image_har_4': imghar4,
                'image_har_5': imghar5,
                'image_har_6': imghar6
            })
