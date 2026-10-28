#!/usr/bin/env python3
"""主题内容文件（示例：积分能量站）。新主题 = 重写本文件 + scenes.json。

必须提供三样东西：
1. SCREENS        —— 16 个屏幕表情模式列表 (id, name, brief, colors, fn)；fn(t) 返回 70×36 面板
2. screen_image(mode, t) + SCREEN_MODES —— 渲染器按此取屏（照抄文件末尾即可）
3. NEW_PROPS      —— 主题专属道具 [(id, builder, name, brief)]；builder() 返回原生像素 PNG
色彩纪律：红/黄/蓝是强调色，只允许出现在 scenes.json design.discipline 登记的幕。
"""
from PIL import Image, ImageDraw

from lib_base import (C, latin, cn_text, panel, osc, blink, outlined, shape, polygon_im,
                      HEART, Z_BIG, STAR,
                      eyes_default, eyes_happy, eyes_star, eyes_heart, eyes_plead,
                      eyes_half, eyes_power, eyes_seed, sparkle)


# =====================================================================
# 屏幕表情：70×36，一幕一屏；t 为循环进度
# =====================================================================

def scr_checkin(t=0.0):
    """01 签到成功：眯眼笑 + 角标 ✓+10。"""
    im = panel(); d = ImageDraw.Draw(im)
    for i in range(3):                                     # 短撇
        d.rectangle((6+i, 6+i, 7+i, 7+i), fill=C['green'])
    for i in range(5):                                     # 长捺
        d.rectangle((8+i, 10-i, 9+i, 11-i), fill=C['green'])
    im.alpha_composite(latin('+10', 'green'), (18, 3))
    if blink(t, 2, 0.7):
        im.alpha_composite(latin('+10', 'mint'), (19, 4))
    eyes_happy(d, 24)
    sparkle(d, 60, 26, t, 2); sparkle(d, 8, 28, t, 3)
    return im


def scr_arrive(t=0.0):
    """02 积分到账：+100 跳字 + 星星眼。"""
    im = panel(); d = ImageDraw.Draw(im)
    im.alpha_composite(latin('+100', 'green', 2), (14, 1+round(osc(t, 2, -2))))
    eyes_star(im, d, t, 25)
    sparkle(d, 6, 8, t, 3); sparkle(d, 62, 8, t, 2, 0.6)
    return im


def scr_grind(t=0.0):
    """03 搬砖赚币：菱形眼 + 砖块与 +1。"""
    im = panel(); d = ImageDraw.Draw(im)
    eyes_default(im, d, t, 15)
    d.rectangle((4, 26, 16, 27), fill=C['shadow'])
    d.rectangle((5, 24, 15, 25), fill=C['shadow'])
    d.rectangle((54, 24, 66, 25), fill=C['shadow'])
    d.rectangle((55, 26, 65, 27), fill=C['shadow'])
    if blink(t, 2, 0.7):
        im.alpha_composite(latin('+1', 'green'), (29, 27))
    sparkle(d, 60, 6, t, 2)
    return im


def scr_invite(t=0.0):
    """04 邀请有礼：眯眼笑 + 像素「来！」。"""
    im = panel(); d = ImageDraw.Draw(im)
    eyes_happy(d, 12)
    lai = cn_text('来！', 'green')
    im.alpha_composite(lai, ((70-lai.width)//2, 19+round(osc(t, 2, -1))))
    sparkle(d, 10, 6, t, 2); sparkle(d, 60, 8, t, 3)
    return im


def scr_fullpower(t=0.0):
    """05 满电开工：100% 满格电池 + 菱形眼。"""
    im = panel(); d = ImageDraw.Draw(im)
    im.alpha_composite(latin('100%', 'white'), (21, 3))
    eyes_default(im, d, t, 22)
    d.rectangle((6, 27, 24, 33), outline=C['white'])
    d.rectangle((25, 29, 26, 31), fill=C['white'])
    for i in range(3):
        d.rectangle((8+i*5, 29, 11+i*5, 31), fill=C['green'])
    if blink(t, 2, 0.5):
        d.rectangle((23, 29, 23, 31), fill=C['mint'])
    sparkle(d, 56, 26, t, 2)
    return im


def scr_burnout(t=0.0):
    """06 火力全开：金色闪电 + 红色 -5 高频坠落 + 急速眨眼。"""
    im = panel(); d = ImageDraw.Draw(im)
    bolt = polygon_im((10, 14), [(8, 0), (2, 7), (5, 7), (0, 14), (9, 5), (6, 5)], 'gold')
    im.alpha_composite(bolt, (56, 2+round(osc(t, 4, 1))))
    eyes_default(im, d, t, 14, fast=True)
    im.alpha_composite(latin('-5', 'red', 2), (20, 20+round(osc(t, 1, 6))))
    for x in (6, 14, 42, 50):
        if blink(t, 3, 0.6):
            d.rectangle((x, 32, x+3, 32), fill=C['shadow'])
    return im


def scr_budget(t=0.0):
    """07 精打细算：半闭眼 + -5 + 迷你计算器。"""
    im = panel(); d = ImageDraw.Draw(im)
    im.alpha_composite(latin('-5', 'green'), (28, 3))
    eyes_half(d, 17)
    d.rectangle((46, 22, 64, 33), outline=C['white'])
    d.rectangle((48, 24, 62, 26), fill=C['green'])
    for row in range(2):
        for col in range(3):
            x, y = 48+col*5, 28+row*3
            d.rectangle((x, y, x+2, y+1), fill=C['shadow'] if (row+col) % 2 else C['mint'])
    if blink(t, 2, 0.5):
        d.rectangle((48, 28, 50, 28), fill=C['green'])
    return im


def scr_topup(t=0.0):
    """08 氪金充值：蓝色像素爱心眼。"""
    im = panel(); d = ImageDraw.Draw(im)
    eyes_heart(im, d, t, 18)
    sparkle(d, 8, 6, t, 2); sparkle(d, 62, 28, t, 3); sparkle(d, 10, 30, t, 2, 0.5)
    return im


def scr_zero_left(t=0.0):
    """09 余额不足：暗淡 0.0.0 闪烁。"""
    im = panel(); d = ImageDraw.Draw(im)
    color = 'green' if blink(t, 2, 0.75) else 'shadow'
    im.alpha_composite(latin('0.0.0', color, 2), (15, 11))
    if blink(t, 3, 0.4):
        d.rectangle((6, 4, 7, 5), fill=C['shadow'])
        d.rectangle((62, 28, 63, 29), fill=C['shadow'])
    return im


def scr_begging(t=0.0):
    """10 求求了：泪眼汪汪，泪滴涨落。"""
    im = panel(); d = ImageDraw.Draw(im)
    eyes_plead(im, d, t)
    sparkle(d, 8, 5, t, 3, 0.5); sparkle(d, 62, 6, t, 2)
    return im


def scr_power_save(t=0.0):
    """11 摆烂省电：单眼待机 + zZ。"""
    im = panel(); d = ImageDraw.Draw(im)
    eyes_power(d, 20)
    im.alpha_composite(shape(Z_BIG, 'mint'), (48, 4+round(osc(t, 1, -2))))
    im.alpha_composite(shape(['###', '..#', '.#.', '###'], 'shadow'), (40, 13))
    if blink(t, 1, 0.3):
        d.rectangle((10, 8, 11, 9), fill=C['green'])
    return im


def scr_crashed(t=0.0):
    """12 当机崩溃：ERR0R 花屏抖动 + 噪点行。"""
    im = panel(); d = ImageDraw.Draw(im)
    dx = round(osc(t, 6, 1))
    im.alpha_composite(latin('ERR0R', 'red'), (13+dx, 5))
    if blink(t, 6, 0.5):
        im.alpha_composite(latin('ERR0R', 'green'), (15+dx, 7))
    shift = int(t*10) % 3
    for i in range(5):
        y = 18+((i*5+shift*2) % 14)
        width = (i*13+shift*5) % 26+6
        d.rectangle((5, y, 5+width, y), fill=C['red'] if (i+shift) % 3 == 0 else C['shadow'])
    for x, y in ((10, 30), (58, 31), (30, 33)):
        if blink(t, 4, 0.5):
            d.rectangle((x, y, x+1, y+1), fill=C['red'])
    return im


def scr_treat(t=0.0):
    """13 俺请客：眯眼笑 + 手心绿色积分币。"""
    im = panel(); d = ImageDraw.Draw(im)
    eyes_happy(d, 12)
    cy = 26+round(osc(t, 2, -1))
    d.ellipse((29, cy-4, 41, cy+6), fill=C['green'])
    d.rectangle((32, cy-2, 38, cy-2), fill=C['ink'])
    d.rectangle((34, cy-2, 35, cy+3), fill=C['ink'])
    d.rectangle((30, cy-4, 31, cy-3), fill=C['white'])
    sparkle(d, 8, 8, t, 2); sparkle(d, 61, 10, t, 3)
    return im


def scr_big_thanks(t=0.0):
    """14 谢谢老板：眯眼笑 + 蓝色小爱心升起。"""
    im = panel(); d = ImageDraw.Draw(im)
    eyes_happy(d, 13)
    mini = shape(HEART, 'blue').resize((9, 8), Image.Resampling.NEAREST)
    if blink(t, 2, 0.7):
        im.alpha_composite(mini, (12, 22+round(osc(t, 2, -2))))
    if blink(t, 2, 0.7, 0.5):
        im.alpha_composite(mini, (50, 24+round(osc(t, 2, -2, 0.5))))
    sparkle(d, 60, 6, t, 2); sparkle(d, 9, 6, t, 3)
    return im


def scr_melon_watch(t=0.0):
    """15 吃瓜围观：瓜籽眼 + o 嘴。"""
    im = panel(); d = ImageDraw.Draw(im)
    eyes_seed(d, t)
    if blink(t, 3, 0.4):
        d.rectangle((8, 6, 9, 7), fill=C['white'])
        d.rectangle((60, 26, 61, 27), fill=C['white'])
    return im


def scr_dream(t=0.0):
    """16 积分自由梦：星星眼 + zZ + 币光。"""
    im = panel(); d = ImageDraw.Draw(im)
    eyes_star(im, d, t, 20)
    im.alpha_composite(shape(Z_BIG, 'mint'), (52, 2+round(osc(t, 1, -2))))
    if blink(t, 2, 0.6):
        d.ellipse((8, 26, 14, 31), fill=C['green'])
        d.rectangle((10, 27, 11, 29), fill=C['ink'])
    sparkle(d, 20, 5, t, 3, 0.5)
    return im


SCREENS = [
    ('checkin', '签到成功', '眯眼笑与 ✓+10 角标', ('green', 'white'), scr_checkin),
    ('arrive', '积分到账', '+100 跳字与星星眼', ('green', 'white'), scr_arrive),
    ('grind', '搬砖赚币', '菱形眼、砖块与 +1', ('green', 'white', 'shadow'), scr_grind),
    ('invite', '邀请有礼', '眯眼笑与像素「来！」', ('green', 'white'), scr_invite),
    ('fullpower', '满电开工', '100% 满格电池', ('white', 'green'), scr_fullpower),
    ('burnout', '火力全开', '金色闪电与红色 -5 坠落', ('gold', 'red', 'white'), scr_burnout),
    ('budget', '精打细算', '半闭眼、-5 与迷你计算器', ('green', 'white', 'mint'), scr_budget),
    ('topup', '氪金充值', '蓝色像素爱心眼', ('blue', 'white'), scr_topup),
    ('zero_left', '余额不足', '暗淡 0.0.0 闪烁', ('green', 'shadow'), scr_zero_left),
    ('begging', '求求了', '泪眼汪汪', ('white', 'blue', 'mint'), scr_begging),
    ('power_save', '摆烂省电', '单眼待机与 zZ', ('mint', 'shadow', 'green'), scr_power_save),
    ('crashed', '当机崩溃', 'ERR0R 花屏抖动', ('red', 'green', 'shadow'), scr_crashed),
    ('treat', '俺请客', '眯眼笑与积分币', ('green', 'white'), scr_treat),
    ('big_thanks', '谢谢老板', '眯眼笑与蓝色小爱心', ('blue', 'white'), scr_big_thanks),
    ('melon_watch', '吃瓜围观', '瓜籽眼与 o 嘴', ('white', 'green', 'mint'), scr_melon_watch),
    ('dream', '积分自由梦', '星星眼、zZ 与币光', ('green', 'mint', 'white'), scr_dream),
]

SCREEN_MODES = {item[0] for item in SCREENS}


def screen_image(mode, t=0.0):
    if mode not in SCREEN_MODES:
        raise ValueError(f'未知屏幕模式：{mode}')
    for item_id, _, _, _, fn in SCREENS:
        if item_id == mode:
            return fn(t)
    raise ValueError(mode)


# =====================================================================
# 主题专属道具：原生整数像素 + 1px 墨黑轮廓
# =====================================================================

COIN_ROWS = [
'....#####....',
'..#########..',
'.###########.',
'.###########.',
'#############',
'#############',
'#############',
'#############',
'#############',
'.###########.',
'.###########.',
'..#########..',
'....#####....']

HEART_ROWS = HEART


def make_coin_t():
    im = shape(COIN_ROWS, 'green')
    d = ImageDraw.Draw(im)
    d.rectangle((4, 4, 8, 5), fill=C['ink'])
    d.rectangle((6, 6, 6, 9), fill=C['ink'])
    d.rectangle((3, 2, 4, 3), fill=C['white'])
    return im


def make_coin_pile_t():
    coin = make_coin_t()
    im = Image.new('RGBA', (29, 21), (0, 0, 0, 0))
    im.alpha_composite(coin, (0, 8))
    im.alpha_composite(coin, (15, 8))
    im.alpha_composite(coin, (7, 0))
    return im


def make_bankcard():
    mask = Image.new('L', (24, 15), 0)
    ImageDraw.Draw(mask).rectangle((0, 0, 23, 14), fill=255)
    im = outlined(mask, 'white')
    d = ImageDraw.Draw(im)
    d.rectangle((2, 4, 21, 6), fill=C['green'])
    d.rectangle((3, 9, 7, 11), fill=C['mint'])
    d.rectangle((12, 9, 20, 10), fill=C['shadow'])
    return im


def make_brick():
    """砖块用纸白主面：与黑色机身拉开对比，贴在躯干前也读得出来。"""
    mask = Image.new('L', (20, 11), 0); d = ImageDraw.Draw(mask)
    d.rectangle((0, 3, 19, 10), fill=255)
    d.rectangle((3, 0, 7, 2), fill=255)
    d.rectangle((12, 0, 16, 2), fill=255)
    im = outlined(mask, 'paper')
    d = ImageDraw.Draw(im)
    d.rectangle((2, 8, 17, 8), fill=C['shadow'])
    d.rectangle((2, 5, 17, 5), fill=C['white'])
    d.rectangle((9, 6, 10, 7), fill=C['ink'])
    return im


def make_watermelon():
    mask = Image.new('L', (24, 20), 0)
    ImageDraw.Draw(mask).pieslice((0, 0, 23, 19), 180, 360, fill=255)
    im = outlined(mask, 'red')
    d = ImageDraw.Draw(im)
    d.rectangle((3, 14, 21, 15), fill=C['white'])
    d.rectangle((3, 16, 21, 17), fill=C['green'])
    for x, y in ((7, 8), (12, 6), (16, 9)):
        d.rectangle((x, y, x+1, y+2), fill=C['ink'])
    return im


def make_hammer():
    mask = Image.new('L', (15, 27), 0); d = ImageDraw.Draw(mask)
    d.rectangle((0, 0, 14, 9), fill=255)
    d.rectangle((6, 10, 8, 26), fill=255)
    im = outlined(mask, 'shell')
    d = ImageDraw.Draw(im)
    d.rectangle((2, 2, 12, 3), fill=C['shadow'])
    d.rectangle((6, 12, 8, 24), fill=C['shadow'])
    d.rectangle((6, 24, 8, 25), fill=C['green'])
    return im


def make_heart_ice():
    return shape(HEART_ROWS, 'blue')


NEW_PROPS = [
    ('coin_t', make_coin_t, '积分币', '能量站通用绿色 T 字积分币'),
    ('coin_pile_t', make_coin_pile_t, '积分币堆', '三枚积分币金字塔'),
    ('bankcard', make_bankcard, '像素银行卡', '氪金充值专用卡'),
    ('brick', make_brick, '像素砖块', '搬砖赚币的砖'),
    ('watermelon', make_watermelon, '像素西瓜', '吃瓜围观专用'),
    ('hammer', make_hammer, '像素打卡锤', '每日签到打卡'),
    ('heart_ice', make_heart_ice, '冰蓝爱心', '感谢老板的像素爱心'),
]
