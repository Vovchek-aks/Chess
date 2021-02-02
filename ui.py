import pygame as pg
from core import *
import os
from ui_settings import *


class UiBord(Bord):
    def __init__(self):
        super().__init__()
        self.select = None

    def draw(self, sc, fn, x, y, s, color):
        sc.blit(fn.render(f'Ход: {self.n_step}{" " * 10} Ходит  {"белый" if color == 1 else "чёрный"}', False, dk_gray),
                (x, y - fn.size('1')[1] - 10))
        c = 1
        for i in range(8):
            for j in range(8):
                pg.draw.rect(sc, (white if c == 1 else dk_gray), (x + s * j,
                                                                  y + s * i,
                                                                  s, s))
                c *= -1

                f = self.grid[i][j]
                sc.blit(FIG_IM_ST[(f.__class__, f.color)], (x + s * j, y + s * i))
            c *= -1


class UiGame:
    def __init__(self, sc, fn, x, y, s):
        self.bord = UiBord()
        self.dr_inf = (sc, fn, x, y, s)

        self.color = 1

    def do_game(self):
        self.bord.draw(*self.dr_inf, self.color)


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
    (Pawn, 1):    pg.transform.scale(load_image('f6.png'), (fig_sz, fig_sz)),
    (Pawn, -1):   pg.transform.scale(load_image('f12.png'), (fig_sz, fig_sz)),
    (Rook, 1):    pg.transform.scale(load_image('f5.png'), (fig_sz, fig_sz)),
    (Rook, -1):   pg.transform.scale(load_image('f11.png'), (fig_sz, fig_sz)),
    (Knight, 1):  pg.transform.scale(load_image('f4.png'), (fig_sz, fig_sz)),
    (Knight, -1): pg.transform.scale(load_image('f10.png'), (fig_sz, fig_sz)),
    (Bishop, 1):  pg.transform.scale(load_image('f3.png'), (fig_sz, fig_sz)),
    (Bishop, -1): pg.transform.scale(load_image('f9.png'), (fig_sz, fig_sz)),
    (King, 1):    pg.transform.scale(load_image('f2.png'), (fig_sz, fig_sz)),
    (King, -1):   pg.transform.scale(load_image('f8.png'), (fig_sz, fig_sz)),
    (Queen, 1):   pg.transform.scale(load_image('f1.png'), (fig_sz, fig_sz)),
    (Queen, -1):  pg.transform.scale(load_image('f7.png'), (fig_sz, fig_sz)),
    (EmptyF, 0):  pg.transform.scale(load_image('empty.png'), (fig_sz, fig_sz))
}


clock = pg.time.Clock()

font = pg.font.Font(None, 24)

game = UiGame(sc, font, *bord_pos, fig_sz)

while True:
    sc.fill(gray)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit(0)

    sc.blit(font.render(str(round(clock.get_fps())), False, red), (width - 50, 30))
    game.do_game()

    pg.display.flip()
    clock.tick(FPS)

