from PIL import Image

im = Image.open('del/freedom-2-v.png')

fill_color = (225, 225, 225)  # your new background color

im = im.convert("RGBA")   # it had mode P after DL it from OP
if im.mode in ('RGBA', 'LA'):
    background = Image.new(im.mode[:-1], im.size, fill_color)
    background.paste(im, im.split()[-1])  # omit transparency
    im = background

im.convert("RGB").save('del/freedom-2-v.jpg')
