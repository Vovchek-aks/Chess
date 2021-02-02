import pygame as pg
from core import *
import os
from ui_settings import *


class UiBord(Bord):
    def draw(self, sc, x, y, s):
        for i in range(9):
            pg.draw.line(sc, dk_gray, (x + i * s, y), (x + i * s, y + s * 8))
            pg.draw.line(sc, dk_gray, (x, y + i * s), (x + s * 8, y + i * s))


def load_image(name, colorkey=None):  # загружает картинки
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        fullname = os.path.join('data', 'sprites', 'shrek3.png')
    image = pg.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pg.init()
sc = pg.display.set_mode(size)


FIG_IM_ST = {
    (Pawn, 1):    load_image('f6.png'),
    (Pawn, -1):   load_image('f12.png'),
    (Rook, 1):    load_image('f5.png'),
    (Rook, -1):   load_image('f11.png'),
    (Knight, 1):  load_image('f4.png'),
    (Knight, -1): load_image('f10.png'),
    (Bishop, 1):  load_image('f3.png'),
    (Bishop, -1): load_image('f9.png'),
    (King, 1):    load_image('f2.png'),
    (King, -1):   load_image('f8.png'),
    (Queen, 1):   load_image('f1.png'),
    (Queen, -1):  load_image('f7.png'),
    (EmptyF, 0):  load_image('empty.png')
}


clock = pg.time.Clock()

font = pg.font.Font(None, 24)

bord = UiBord()

while True:
    sc.fill(gray)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit(0)

    sc.blit(font.render(str(round(clock.get_fps())), False, red), (width - 50, 30))
    bord.draw(sc, 50, 50, 50)

    pg.display.flip()
    clock.tick(FPS)

