from slugify import slugify

txt = 'приїхав і й іііі щаовла, ю. єваерест, їіїіїії єжвд(кккккк)'
r = slugify(txt, replacements=[['Ü', 'UE'], ['ü', 'ue'], ['і', 'i2'], ['ї', 'i'], ['є', 'e']])
print(r)
