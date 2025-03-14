#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
identicon.py
模块化设计，支持命令行参数：
  -c CODE   : 输入码（字符串）
  -s SIZE   : 块大小（默认24）
  -f FILE   : 保存路径（优先级最高）
  -n        : 不自动保存（优先级次之）
  -r        : 直接显示图片（独立逻辑）
"""

import argparse
import hashlib
import sys
from PIL import Image, ImageDraw, ImagePath, ImageColor

__all__ = ['render_identicon', 'IdenticonRendererBase']


class Matrix2D(list):
    """Matrix for Patch rotation"""

    def __init__(self, initial=[0.] * 9):
        assert isinstance(initial, list) and len(initial) == 9
        super().__init__(initial)

    def clear(self):
        for i in range(9):
            self[i] = 0.

    def set_identity(self):
        self.clear()
        for i in range(3):
            self[i] = 1.

    def __str__(self):
        return '[%s]' % ', '.join('%3.2f' % v for v in self)

    def __mul__(self, other):
        r = []
        if isinstance(other, Matrix2D):
            for y in range(3):
                for x in range(3):
                    v = 0.0
                    for i in range(3):
                        v += (self[i * 3 + x] * other[y * 3 + i])
                    r.append(v)
        else:
            raise NotImplementedError()
        return Matrix2D(r)

    def for_PIL(self):
        return self[0:6]

    @classmethod
    def translate(kls, x, y):
        return kls([1.0, 0.0, float(x),
                    0.0, 1.0, float(y),
                    0.0, 0.0, 1.0])

    @classmethod
    def scale(kls, x, y):
        return kls([float(x), 0.0, 0.0,
                    0.0, float(y), 0.0,
                    0.0, 0.0, 1.0])

    @classmethod
    def rotateSquare(kls, theta, pivot=None):
        theta = theta % 4
        c = [1., 0., -1., 0.][theta]
        s = [0., 1., 0., -1.][theta]

        matR = kls([c, -s, 0., s, c, 0., 0., 0., 1.])
        if not pivot:
            return matR
        return kls.translate(-pivot[0], -pivot[1]) * matR * \
            kls.translate(*pivot)


class IdenticonRendererBase(object):
    PATH_SET = []

    def __init__(self, code):
        if not isinstance(code, str):
            code = str(code)
        self.code = code

    def render(self, size):
        # decode the code
        middle, corner, side, foreColor, backColor = self.decode(self.code)

        # make image
        image = Image.new("RGB", (size * 3, size * 3))
        draw = ImageDraw.Draw(image)

        # fill background
        draw.rectangle((0, 0, image.size[0], image.size[1]), fill=backColor)

        kwds = {
            'draw': draw,
            'size': size,
            'foreColor': foreColor,
            'backColor': backColor}
        # middle patch
        self.drawPatch((1, 1), middle[2], middle[1], middle[0], **kwds)

        # side patch
        kwds['type'] = side[0]
        for i in range(4):
            pos = [(1, 0), (2, 1), (1, 2), (0, 1)][i]
            self.drawPatch(pos, side[2] + 1 + i, side[1], **kwds)

        # corner patch
        kwds['type'] = corner[0]
        for i in range(4):
            pos = [(0, 0), (2, 0), (2, 2), (0, 2)][i]
            self.drawPatch(pos, corner[2] + 1 + i, corner[1], **kwds)

        return image

    def drawPatch(self, pos, turn, invert, type, draw, size, foreColor, backColor):
        path = self.PATH_SET[type]
        if not path:
            invert = not invert
            path = [(0., 0.), (1., 0.), (1., 1.), (0., 1.), (0., 0.)]
        patch = ImagePath.Path(path)
        if invert:
            foreColor, backColor = backColor, foreColor

        mat = Matrix2D.rotateSquare(turn, pivot=(0.5, 0.5)) *\
            Matrix2D.translate(*pos) *\
            Matrix2D.scale(size, size)

        patch.transform(mat.for_PIL())
        draw.rectangle((pos[0] * size, pos[1] * size, (pos[0] + 1) * size,
                        (pos[1] + 1) * size), fill=backColor)
        draw.polygon(patch, fill=foreColor, outline=foreColor)

    def decode(self, code):
        raise NotImplementedError()


class DonRenderer(IdenticonRendererBase):
    PATH_SET = [
        [(0, 0), (4, 0), (4, 4), (0, 4)],   # 0
        [(0, 0), (4, 0), (0, 4)],
        [(2, 0), (4, 4), (0, 4)],
        [(0, 0), (2, 0), (2, 4), (0, 4)],
        [(2, 0), (4, 2), (2, 4), (0, 2)],   # 4
        [(0, 0), (4, 2), (4, 4), (2, 4)],
        [(2, 0), (4, 4), (2, 4), (3, 2), (1, 2), (2, 4), (0, 4)],
        [(0, 0), (4, 2), (2, 4)],
        [(1, 1), (3, 1), (3, 3), (1, 3)],   # 8
        [(2, 0), (4, 0), (0, 4), (0, 2), (2, 2)],
        [(0, 0), (2, 0), (2, 2), (0, 2)],
        [(0, 2), (4, 2), (2, 4)],
        [(2, 2), (4, 4), (0, 4)],
        [(2, 0), (2, 2), (0, 2)],
        [(0, 0), (2, 0), (0, 2)],
        []]                                 # 15

    MIDDLE_PATCH_SET = [0, 4, 8, 15]

    # modify path set
    for idx in range(len(PATH_SET)):
        if PATH_SET[idx]:
            p = list(
                map(lambda vec: (vec[0] / 4.0, vec[1] / 4.0), PATH_SET[idx]))
            PATH_SET[idx] = p + p[:1]

    def decode(self, code):
        code_int = string_to_int(code)
        middleType = self.MIDDLE_PATCH_SET[code_int & 0x03]
        middleInvert = (code_int >> 2) & 0x01
        cornerType = (code_int >> 3) & 0x0F
        cornerInvert = (code_int >> 7) & 0x01
        cornerTurn = (code_int >> 8) & 0x03
        sideType = (code_int >> 10) & 0x0F
        sideInvert = (code_int >> 14) & 0x01
        sideTurn = (code_int >> 15) & 0x03
        blue = (code_int >> 16) & 0x1F
        green = (code_int >> 21) & 0x1F
        red = (code_int >> 27) & 0x1F

        foreColor = (red << 3, green << 3, blue << 3)

        return ((middleType, middleInvert, 0),
                (cornerType, cornerInvert, cornerTurn),
                (sideType, sideInvert, sideTurn),
                foreColor, ImageColor.getrgb('white'))


def string_to_int(s: str) -> int:
    """将字符串转换为唯一的整数（SHA-256哈希）"""
    hash_bytes = hashlib.sha256(s.encode()).digest()
    return int.from_bytes(hash_bytes, byteorder='big')


def render_identicon(code, size, renderer=None):
    if not renderer:
        renderer = DonRenderer
    return renderer(code).render(size)


def main():
    parser = argparse.ArgumentParser(description='生成Identicon图标')
    parser.add_argument('-c', '--code', required=True, help='输入码（字符串）')
    parser.add_argument('-s', '--size', type=int, default=24, help='块大小（默认24）')
    parser.add_argument('-f', '--file', help='保存路径（优先级最高）')
    parser.add_argument('-n', '--no-save', action='store_true', help='禁止默认保存')
    parser.add_argument('-r', '--show', action='store_true', help='直接显示图片')

    args = parser.parse_args()

    # 生成图像
    img = render_identicon(args.code, args.size)

    # 保存逻辑（优先级：-f > -n > 默认保存）
    if args.file:
        img.save(args.file)
        print(f"保存至: {args.file}")
    elif not args.no_save:
        filename = f"{string_to_int(args.code):08x}.png"
        img.save(filename)
        print(f"保存至: {filename}")

    # 显示逻辑（独立于保存）
    if args.show:
        img.show()


if __name__ == '__main__':
    main()
