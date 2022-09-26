# from slugify import slugify

# txt = 'ЛІЖКО АЙРІС (З ПІДЙОМНИМ МЕХАНІЗМОМ ЛІЖКО ОЛЬГА - 0,9М М"які ліжка)'
# r = slugify(txt, replacements=[['Ü', 'UE'], ['ü', 'ue'], ['і', 'i'], ['І', 'I'],
#                                ['ї', 'i'], ['є', 'e'], ['є', 'e'], ["'", '']])
# print(r)

img = 0

for i in range(1, 12):
    if i < len_all_images_name:
        img[i] = all_images_name[i]
    else:
        img[i] = '0'
