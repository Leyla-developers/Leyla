# https://ru.stackoverflow.com/questions/581788/Как-создать-круглый-портрет-в-pil
from PIL import Image, ImageDraw
from io import BytesIO


import disnake


def prepare_mask(size, antialias = 2):
    mask = Image.new('L', (size[0] * antialias, size[1] * antialias), 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
    return mask.resize(size, Image.ANTIALIAS)

def crop(im, s):
    w, h = im.size
    k = w / s[0] - h / s[1]
    if k > 0: im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
    elif k < 0: im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
    return im.resize(s, Image.ANTIALIAS)

def get_mask():
    size = (420, 420)
    im = Image.open('rounded_thumbnail.png')
    im = crop(im, size)
    im.putalpha(prepare_mask(size, 4))
    im.save('rounded_thumbnail.png')
    return 