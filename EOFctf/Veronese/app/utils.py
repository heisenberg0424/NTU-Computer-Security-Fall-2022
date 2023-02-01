from PIL import Image, ImageChops, ImageDraw, ImageFont

from hashlib import sha256
from typing import Dict, IO, Optional, Union

MAX_LEN = 180
FONT_WIDTH = 24
FONT_HEIGHT = FONT_WIDTH * 2
FONT_SIZE = FONT_HEIGHT
FONT_FILE = './static/Inconsolata-Regular.ttf'
ACCEPTABLE_ASCII = " 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

def is_same_image(img1: Image.Image, img2: Image.Image) -> bool:
    return ImageChops.difference(img1, img2).getbbox() == None


def texts_to_image(texts: Union[list[str], list[bytes]],
                   rows: int = 3,
                   cols: int = MAX_LEN) -> Optional[Image.Image]:
    img = Image.new("RGB", (cols * FONT_WIDTH, rows * FONT_HEIGHT),
                    (255, 255, 255))

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_FILE, FONT_SIZE)

    for i, s in enumerate(texts):
        if i == rows:
            return None
        if isinstance(s, bytes):
            try:
                s = s.decode('ascii')
            except:
                return None
        if len(s) > cols:
            return None
        draw.text((0, i * FONT_HEIGHT), s, (0, 0, 0), font)

    return img


def image_to_texts(img: Image.Image, rows: int = 3, cols: int = MAX_LEN) -> list[str]:
    char_map : Dict[str, Image.Image] = {}
    for char in ACCEPTABLE_ASCII:
        char_map[char] = texts_to_image([char], 1, 1)

    texts : list[str] = []
    for h in range(rows):
        texts.append("")
        for w in range(cols):
            target_img = img.crop(
                (w * FONT_WIDTH, h * FONT_HEIGHT, w * FONT_WIDTH + FONT_WIDTH,
                 h * FONT_HEIGHT + FONT_HEIGHT))
            for char, char_img in char_map.items():
                if is_same_image(char_img, target_img):
                    texts[-1] += char
                    break
        texts[-1] = texts[-1].strip()
    return texts


def is_docstring(texts: list[str]) -> bool:
    if len(texts) != 3:
        return False
    if texts[0] != "'''":
        return False
    if texts[2] != "'''":
        return False
    if "'" in texts[1]:
        return False
    return True


def sha256sum(io: IO):
    h = sha256()
    h.update(io.read())
    io.seek(0)
    return h.hexdigest()
