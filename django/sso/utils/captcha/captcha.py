# 用于生成验证码图像'
import base64
import random
import string
import os
import uuid
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
FONT_PATH = os.path.join(os.path.dirname(__file__), 'fonts')
import config


# 生成随机字符
def random_char():
    # return random.sample(
        # string.ascii_uppercase + string.ascii_uppercase + '3456789', 4)
    return random.choice(string.ascii_uppercase + string.ascii_uppercase + '23456789')


def random_bg_color():
    return random.randint(126, 255), random.randint(126, 255), random.randint(126, 255)


def random_font_color():
    return random.randint(10, 66), random.randint(10, 66), random.randint(10, 66)


# 创建一个字体对象
def random_font(min_size=28, max_size=34, rnd=True):
    fonts = []
    for font in ['Arial.ttf', 'Georgia.ttf', 'actionj.ttf']:
        fonts.append(os.path.join(FONT_PATH, font))

    font_type = fonts[random.randint(0, len(fonts)-1)]
    font_size = (max_size + min_size) >> 1

    if rnd:
        font_size = random.randint(min_size, max_size)
    return ImageFont.truetype(font_type, font_size, encoding='utf-8')


def create_verify(max_size=34, length=config.img_verify_code_length):
    left_space, top_space = int(max_size >> 1), int(max_size >> 2)
    width, height = max_size * length + left_space * 2, max_size + top_space

    """ 创建图片 """
    # 创建一个图片数据
    img = Image.new('RGB', (width, height))
    # 为图片分配存储空间和并加载像素数据
    pixs = img.load()
    # 绘制图像
    draw = ImageDraw.Draw(img)
    for x in range(width):
        for y in range(height):
            pixs[x, y] = random_bg_color()

    ret_code = ''
    last_right = 0
    # 将文字吸入到图片中去
    for i in range(length):
        char = random_char()
        ret_code += char
        font = random_font(min_size=max_size - 6, max_size=max_size, rnd=True)
        font_width, font_height = font.getsize(char)
        if i == 0:
            last_right = left_space + ((max_size - font_width) >> 1) \
                         + font_width
            draw.text(((left_space + (max_size - font_width) >> 1),
                      top_space - random.randint(6,12)),
                      char, file=random_font_color, font=font)
        else:
            offset = random.randint(1, 6)
            draw.text((last_right - offset, top_space - random.randint(6, 12)), char,
                      fill=random_font_color(), font=font)
            last_right += (font_width - offset)

    del draw
    region = (0, 0, max(last_right + left_space, 100 + left_space), height)
    # 裁剪图片
    crop_img = img.crop(region)

    # 将图片写入二进制缓存中
    buffered = BytesIO()
    crop_img.save(buffered, format='JPEG')
    # 返回验证码图片对应的验证码， 图片二进制文件
    return ret_code, buffered.getvalue()


# 测试代码
# a = create_verify()
# with open('test.jpg', 'wb') as f:
#     f.write(a[1])
# print(a[0], a[1])

