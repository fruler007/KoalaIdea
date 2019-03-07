import base64
import random
import string
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont



_FONT_PATH = os.path.join(__file__, 'font')  # 这个是字体的存储路径，根据实际填写


# 产生随机字符（大小写字母或数字）
def rnd_char():
    return random.choice(string.ascii_letters + string.digits)


# 产生随机颜色（颜色较浅，用于产生背景干扰颜色） 实际上这个对增加自动识别的难度几乎没有任何作用
def rnd_bg_color():
    return random.randint(126, 255), random.randint(126, 255), random.randint(126, 255)


# 产生随机颜色（颜色较深，用于产生验证码字符颜色）
def rnd_ch_color():
    return random.randint(10, 66), random.randint(10, 66), random.randint(10, 66)


# 产生随机字体 字体可以自己去网上下载，尽量不要太规范的字体
def rnd_font(min_size=28, max_size=34, rnd=True):
    font_types = (_FONT_PATH + 'actionj.ttf', _FONT_PATH + 'Arial.ttf',
                  _FONT_PATH + 'Georgia.ttf',)
    font_type = font_types[random.randint(0, len(font_types) - 1)]
    font_size = (max_size + min_size) >> 1
    if rnd:
        font_size = random.randint(min_size, max_size)
    return ImageFont.truetype(font_type, font_size, encoding='utf-8')


# 生产验证码图片，返回图片对应的验证码
def create_verification(max_size=34, length=4):
    left_space, top_space = int(max_size >> 1), int(max_size >> 2)
    print('left space: {0}, top_space: {1}'.format(left_space, top_space))
    width, height = max_size * length + left_space * 2, max_size + top_space  # 图片的大小比验证码大小稍大
    # 创建初始图片
    img = Image.new('RGB', (width, height))
    pixs = img.load()
    draw = ImageDraw.Draw(img)
    # 画背景颜色
    for i in range(width):
        for j in range(height):
            pixs[i, j] = rnd_bg_color()
    ret_code = ''
    last_right = 0
    # 画验证码 TODO: 字体小角度旋转没完成
    for i in range(length):
        code = rnd_char()
        ret_code += code
        font = rnd_font(min_size=max_size - 6, max_size=max_size, rnd=True)
        font_width, font_height = font.getsize(code)
        if i == 0:
            last_right = left_space + ((max_size - font_width) >> 1) + font_width
            draw.text((left_space + ((max_size - font_width) >> 1), top_space - random.randint(6, 12)),
                      code, fill=rnd_ch_color(), font=font)
        else:
            offset = random.randint(1, 6)
            draw.text((last_right - offset, top_space - random.randint(6, 12)), code,
                      fill=rnd_ch_color(), font=font)
            last_right += (font_width - offset)
    # 画干扰线，很难看暂时不用
    # for k in range(2):
    #     draw.line(((0, random.randint(2, max_size - 2)), (length * max_size, random.randint(0, max_size))),
    #               rnd_bg_color(), 1)
    del draw
    region = (0, 0, max(last_right + left_space, 100 + left_space), height)
    # 裁切图片
    crop_img = img.crop(region)
    # 这里直接返回图片的data数据，符合网站验证码实际要求
    buffered = BytesIO()
    crop_img.save(buffered, format="JPEG")
    return 'data:image/png;base64,' + base64.b64encode(buffered.getvalue()).decode(encoding="utf-8"), ret_code

a = create_verification()
with open('test', 'r') as f:
    f.write(a)