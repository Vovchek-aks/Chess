import pygame as pg
from core import *
import os
from ui_settings import *


class UiBord(Bord):
    def __init__(self):
        super().__init__()

    def draw(self, sc, fn, x, y, s, color):
        sc.blit(fn.render(f'Ход: {self.n_step}{" " * 10} Ходит  {"белый" if color == 1 else "чёрный"}', False, black),
                (x, y - fn.size('1')[1] - 10))
        c = 1
        for i in range(8):
            for j in range(8):
                pg.draw.rect(sc, (white if c == 1 else dk_gray), (x + s * j,
                                                                  y + s * i,
                                                                  s, s))
                c *= -1

                f = self.grid[i][j]
                if f.__class__ != EmptyF:
                    sc.blit(FIG_IM_ST[(f.__class__, f.color)], (x + s * j, y + s * i))

            sc.blit(fn.render(str(8 - i), False, black), (x - 20, y + s // 2.5 + s * i))
            sc.blit(fn.render(str(i + 1), False, black), (x + s // 2.5 + s * i, y + s * 8 + 10))
            c *= -1

        sc.blit(fn.render('Потери:', False, black), (x + s * 8 + 40, y - fn.size('1')[1] - 10))
        for i in range(len(self.lose[1])):
            sc.blit(FIG_IM_ST[(self.lose[1][i], 1)], (x + s * 8 + 40, y + s * i))
        for i in range(len(self.lose[-1])):
            sc.blit(FIG_IM_ST[(self.lose[-1][i], -1)], (x + s * 8 + 50 + fig_sz, y + s * i))


class UiGame:
    def __init__(self, sc, fn, x, y, s):
        self.bord = UiBord()
        self.b_inf = x, y, s
        self.dr_inf = sc, fn, *self.b_inf

        self.color = 1

        self.select_pos = None

    def draw(self):
        if self.select_pos is not None:
            pos = self.select_pos[0] * self.b_inf[2] + self.b_inf[0], \
                  self.select_pos[1] * self.b_inf[2] + self.b_inf[1]
            s = pg.Surface((self.b_inf[2], self.b_inf[2]))
            s.set_alpha(150)
            s.fill(yellow)
            sc.blit(s, pos)

            for i in self.bord.grid[self.select_pos[1]][self.select_pos[0]].go_pos(self.bord):
                pos = i[1] * self.b_inf[2] + self.b_inf[0], \
                      i[0] * self.b_inf[2] + self.b_inf[1]
                s = pg.Surface((self.b_inf[2], self.b_inf[2]))
                s.set_alpha(150)
                if self.bord.grid[i[0]][i[1]].__class__ == EmptyF:
                    s.fill(lime)
                else:
                    s.fill(red)
                sc.blit(s, pos)

    def do_game(self):
        self.bord.draw(*self.dr_inf, self.color)
        self.draw()
        if self.bord.is_win(-self.color):
            return True
        return False

    def click(self, x, y):
        xx = (x - self.b_inf[0]) // self.b_inf[2]
        yy = (y - self.b_inf[1]) // self.b_inf[2]
        if 0 <= xx < 8 and 0 <= yy < 8:
            f = self.bord.grid[yy][xx]
            if f.go_pos(self.bord) and f.color == self.color:
                self.select_pos = xx, yy
            elif self.select_pos is not None and (yy, xx) in \
                    self.bord.grid[self.select_pos[1]][self.select_pos[0]].go_pos(self.bord):
                self.bord.step(self.color, *self.select_pos[::-1], yy, xx)
                self.select_pos = None
                self.color *= -1
            else:
                self.select_pos = None
        else:
            self.select_pos = None


def load_image(name, colorkey=None):  # загружает картинки
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
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

pg.display.set_caption('Chess')

FIG_IM_ST = {
    (Pawn, 1): pg.transform.scale(load_image('f6.png'), (fig_sz, fig_sz)),
    (Pawn, -1): pg.transform.scale(load_image('f12.png'), (fig_sz, fig_sz)),
    (Rook, 1): pg.transform.scale(load_image('f5.png'), (fig_sz, fig_sz)),
    (Rook, -1): pg.transform.scale(load_image('f11.png'), (fig_sz, fig_sz)),
    (Knight, 1): pg.transform.scale(load_image('f4.png'), (fig_sz, fig_sz)),
    (Knight, -1): pg.transform.scale(load_image('f10.png'), (fig_sz, fig_sz)),
    (Bishop, 1): pg.transform.scale(load_image('f3.png'), (fig_sz, fig_sz)),
    (Bishop, -1): pg.transform.scale(load_image('f9.png'), (fig_sz, fig_sz)),
    (King, 1): pg.transform.scale(load_image('f2.png'), (fig_sz, fig_sz)),
    (King, -1): pg.transform.scale(load_image('f8.png'), (fig_sz, fig_sz)),
    (Queen, 1): pg.transform.scale(load_image('f1.png'), (fig_sz, fig_sz)),
    (Queen, -1): pg.transform.scale(load_image('f7.png'), (fig_sz, fig_sz))
}

clock = pg.time.Clock()

font = pg.font.Font(None, 24)
font2 = pg.font.Font(None, 48)

game = UiGame(sc, font, *bord_pos, fig_sz)

while True:
    sc.fill(gray)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit(0)
        elif event.type == pg.MOUSEBUTTONDOWN:
            game.click(*event.pos)

    # sc.blit(font.render(str(round(clock.get_fps())), False, red), (width - 50, 30))

    if game.do_game():
        t = f'Победил {"белый" if game.color == -1 else "чёрный"}'
        color = white if game.color == -1 else black
        sc.blit(font2.render(t, False, color), (width - font2.size(t)[0] - 50,
                                                height - font2.size(t)[1] - 10))
        pg.display.flip()
        f = True
        while f:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit(0)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    f = False
                    break

        game = UiGame(sc, font, *bord_pos, fig_sz)

    pg.display.flip()
    clock.tick(FPS)
