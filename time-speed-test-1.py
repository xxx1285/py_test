from datetime import datetime
import time
# from csv import reader
from bs4 import BeautifulSoup
import requests
import csv
from fake_useragent import UserAgent

url = "https://cosmohit.ua/catalogue/cream/brand-zein_obagi"


headers = {
    'user-agent': UserAgent().random
}
# print(headers)

response = requests.get(url, headers=headers).text

# with open('111.csv', 'w', encoding='utf-8') as file:
#     file.write(response)

soup_respon = BeautifulSoup(response, 'lxml')

# all_select = soup_respon.select(".items > div > a")

with open('111.csv', 'w', encoding='utf-8') as file:
    field_names = ['name', 'name_original', 'href', 'img', 'price']
    csv_writer = csv.DictWriter(file, fieldnames=field_names)
    # csv_writer.writerow(['link', 'src', 'alt'])
    for bit in soup_respon.select(".items > div"):
        # result_href = link_a.get('href')
        prod_href = bit.find('a').get('href')

        prod_name = bit.select_one(
            'a > span:last-child > span:first-child').get_text()
        # prod_name_bit = prod_name
        prod_name_original = bit.select_one(
            'a>span:last-child>span:nth-child(2)').get_text()

        print(prod_name)
        print(prod_name_original)

        # result_alt = bit.get('alt')

        # csv_writer.writerow({'src': result_src, 'alt': result_src1})


# with open('111.csv', 'w', encoding='utf-8') as file:
#     field_names = ['src', 'alt']
#     csv_writer = csv.DictWriter(file, fieldnames=field_names)
#     # csv_writer.writerow(['link', 'src', 'alt'])
#     for link_a in all_product_img:
#         # result_href = link_a.get('href')
#         result_src = link_a.get('src')
#         result_alt = link_a.get('alt')
#         csv_writer.writerow({'src': result_src, 'alt': result_alt})


# with open('111.csv', 'w', encoding='utf-8') as file:
#     csv_writer = csv.writer(file, delimiter=';')
#     csv_writer.writerow(['link', 'src', 'alt'])
#     for link_a in all_select:
#         result_url = link_a.get('src')
#         result_url2 = link_a.get('alt')
#         csv_writer.writerow([result_url + ';' + result_url2])


# with open('111.csv', 'w', encoding='utf-8') as file:
#     file.write(str(all_select))
# 122312123123

# with open('111.csv', 'w', encoding='utf-8') as file:
#     file.write(str(all_select))
#     for link_a in all_select:
#         result_url = link_a.get('src')
#         print('www' + result_url)
#         result_url2 = link_a.get_text()
#         print(result_url2)
#         file.write(str(result_url))
# file.write(str(result_url2))
# file.write(result_url, delimiter=";")
# writer = csv.writer(file, delimiter =";",quoting=csv.QUOTE_MINIMAL)
# writer.writerow(["a","b"])

        # csv_writer.writerow([result_url2])

start_time = datetime.now()

#Тут выполняются действия
time.sleep(5)

print(datetime.now() - start_time)
