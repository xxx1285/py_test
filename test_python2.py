# from PIL import Image

# im = Image.open('del/freedom-2-v.png')

# fill_color = (225, 225, 225)  # your new background color

# im = im.convert("RGBA")   # it had mode P after DL it from OP
# if im.mode in ('RGBA', 'LA'):
#     background = Image.new(im.mode[:-1], im.size, fill_color)
#     background.paste(im, im.split()[-1])  # omit transparency
#     im = background

# im.convert("RGB").save('del/freedom-2-v.jpg')

# box_numbers = [1, 2, 3, 4, 10, 123, 122, 123, 123, 190]

# coordinates = [0, 5] 
# commands = ["back", "back", "back", "back", "back"]

# def get_location(coordinates: list, commands: list) -> list:
#     # write your code here
#     x = 0
#     y = 0
#     forvard = [x + 0, y + 1]
#     back = [x + 0, y - 1]
#     right = [x + 1, y + 0]
#     left = [x - 1, y + 0]

#     result_coordinates = []

#     for i in range(len(commands)):
#         if commands[i] == "forward":
#             result_coordinates = (coordinates[0] + 0, coordinates[1] + 1)
#         if commands[i] == "back":
#             result_coordinates = (coordinates[0] + 0, coordinates[1] - 1)
#         if commands[i] == "right":
#             result_coordinates = (coordinates[0] + 1, coordinates[1] + 0)            
#         if commands[i] == "left":
#             result_coordinates = (coordinates[0] - 1, coordinates[1] + 0)
#         print(i)
#         print(commands[i])
#         print(result_coordinates)
#     return result_coordinates
#     print(result_coordinates)

# get_location([0, 5], ["back", "back", "back", "back", "back"])

# def get_location(coordinates: list, commands: list) -> list:
#     # write your code here
#     x = 0
#     y = 0
#     forvard = [x + 0, y + 1]
#     back = [x + 0, y - 1]
#     right = [x + 1, y + 0]
#     left = [x - 1, y + 0]

#     # result_coordinates = []

#     for i in range(len(commands)):
#         if commands[i] == "forward":
#             coordinates = [coordinates[0] + 0, coordinates[1] + 1]
#         if commands[i] == "back":
#             coordinates = [coordinates[0] + 0, coordinates[1] - 1]
#         if commands[i] == "right":
#             coordinates = [coordinates[0] + 1, coordinates[1] + 0]            
#         if commands[i] == "left":
#             coordinates = [coordinates[0] - 1, coordinates[1] + 0]
#         print(i)
#         print(commands[i])
#         print(coordinates)
#     return coordinates
#     print(coordinates)

# get_location([0, 5], ["back", "back", "back", "back", "back"])

# def www123(x):
#     dd = x * 123
#     ff = x * 345
#     return ff


# s = www123(2)
# print(s)
# print(type(s))

import math


def get_plan(current_production: int, month: int, percent: int):
    # write your code here
    result_get_plan = []

    for i in range(month):
        current_production = round((current_production / 100) * percent)
        # result_get_plan.ap
        result_get_plan = result_get_plan.append(current_production)
        return result_get_plan
        print(i)
        print(result_get_plan)
