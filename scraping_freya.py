

from csv import reader
from bs4 import BeautifulSoup
import requests
# import csv
# from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ua = UserAgent()


url = "https://freyamebel.com/"
headers = {
    'user-agent': ua.random
}
print(headers)

response = requests.get(url, headers=headers).text
"""Делаем запрос по url + hesders"""

with open('111.csv', 'w', encoding='utf-8') as file:
    file.write(response)

soup_respon = BeautifulSoup(response, 'lxml')

# response2 = requests.get(url, 'lxml', headers=headers).text
# status_url = requests.get(url, 'lxml', headers=headers).status_code

# all_select = soup_respon.select(".items > div > a")
all_select = soup_respon.select(".category-wall > a")

# with open('111.csv', 'w', encoding='utf-8') as file:
#     file.write(str(all_select))

with open('111.csv', 'a', encoding='utf-8') as file:
    file.write(str(all_select))
    for link_a in all_select:
        result_url = link_a.get_text()
        print(result_url)
        # file.write(result_url, delimiter=";")
        # writer = csv.writer(file, delimiter =";",quoting=csv.QUOTE_MINIMAL)
        # writer.writerow(["a","b"])
    # for link_a in all_select:
    #     print(str(link_a))


# for link_a in all_select:
#     with open('111.csv', 'w', encoding='utf-8') as file:
#         file.write(str(link_a))
#         print(link_a)

# def fun_csv_noda()
#     for link in all_select:
#         # rars = link.select("li")
#         csv_noda = link.get_text()
#         print(csv_noda)
#         return csv_noda

print(type(response))
print(type(soup_respon))
print(type(all_select))
# print(response2)
# print(status_url)

# keyss = {'ddd': 'ffff', 'sss': 'gggg'}
# response2 = requests.get(url, params=keyss)


# with open('1285888.csv', 'w', encoding='utf-8') as zalupa:
#     zalupa.write(response)


# if response.status_code == 300:
#     print('Hello! Nice to meet you!')
# else:
#     print('ERROR - ' + str(response.status_code))

# html_data = BeautifulSoup(response.text)

# all_items = html_data.find_all(class_='items')


# all_item_a = all_items.select('a > span > span:first-child')
# print(all_item_a.get_text())
# print(type(all_item_a))

# for link in all_select:
#     print(link.select('a > span > span:first-child'))
#     print(type(link.select('a > span > span:first-child')))
# for link in all_select:
#     print(link.get_text())
# for item in all_items:
# item.select('a > span > span:first-child')
# print(item)


# print(all_select)
# print(type(response))

# print(type(response.text))
# print(response.status_code)
# print(response.text)
