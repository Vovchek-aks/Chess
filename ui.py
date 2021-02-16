import pygame as pg
from core import *
import os
from ui_settings import *
from time import sleep


class UiBord(Bord):
    def __init__(self, grid=None):
        super().__init__(grid)

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
            alf = 'ABCDEFGH'
            sc.blit(fn.render(alf[i], False, black), (x + s // 2.5 + s * i, y + s * 8 + 10))
            c *= -1

        sc.blit(fn.render('Потери:', False, black), (x + s * 8 + 40, y - fn.size('1')[1] - 10))
        for i in range(len(self.lose[1])):
            sc.blit(FIG_IM_ST[(self.lose[1][i], 1)], (x + s * 8 + 40, y + s * i))
        for i in range(len(self.lose[-1])):
            sc.blit(FIG_IM_ST[(self.lose[-1][i], -1)], (x + s * 8 + 50 + fig_sz, y + s * i))


class Player:
    def __init__(self, bord, color):
        self.bord = bord
        self.color = color

    def get_step(self):
        pass

    def draw(self):
        return ()


class PlayerP(Player):
    def __init__(self, bord, color):
        super().__init__(bord, color)

        self.select_pos = None
        self.step = None

    def draw(self):
        ret = []
        if self.select_pos is not None:
            ret += [(self.select_pos[::-1], yellow)]

            for i in self.bord.grid[self.select_pos[1]][self.select_pos[0]].go_pos(self.bord):
                if self.bord.grid[i[0]][i[1]].__class__ == EmptyF:
                    c = lime
                else:
                    c = red
                ret += [(i, c)]
        return ret

    def click(self, x, y):
        if 0 <= x < 8 and 0 <= y < 8:
            f = self.bord.grid[y][x]
            if f.go_pos(self.bord) and f.color == self.color:
                self.select_pos = x, y
            elif self.select_pos is not None and (y, x) in \
                    self.bord.grid[self.select_pos[1]][self.select_pos[0]].go_pos(self.bord):
                self.step = x, y
            else:
                self.select_pos = None
        else:
            self.select_pos = None

    def get_step(self, pos=(0, 0)):
        if self.step:
            r = self.select_pos, self.step
            self.select_pos = None
            self.step = None
            return r


class PlayerAi(Player):
    def get_figs(self, bord):
        figs = []
        for i in bord:
            if i.color == self.color:
                figs += [i]
        return figs

    def get_steps(self, figs):
        s = []
        for i in figs:
            for j in i.go_pos(self.bord):
                s += [(*i.pos, *j)]
        return s

    def cost(self, bord):
        summ = 0
        for i in self.get_figs(bord):
            for j in self.get_steps([i]):
                summ += get_cost(bord.grid[j[2]][j[3]].__class__, i.color != self.color) + randint(0, 20)
        return summ

    def get_step(self, pos=(0, 0)):
        99**99
        figs = self.get_figs(self.bord)
        hods = []
        for i in self.get_steps(figs):
            b = Bord(self.bord.grid)
            # print(b is self.bord)
            b.step(self.color, *i)
            hods += [((i[0:2][::-1], i[2:][::-1]), self.cost(b))]

        ret = sorted(hods, key=lambda x: x[1])
        print(ret)
        return ret[0][0]


class UiGame:
    def __init__(self, sc, fn, x, y, s, players):
        self.bord = UiBord()
        self.b_inf = x, y, s
        self.dr_inf = sc, fn, *self.b_inf

        self.click_pos = (0, 0)

        self.players = {
            +1: players[0](self.bord, +1),
            -1: players[1](self.bord, -1)
        }

        self.color = 1

    def draw(self, to_dr=()):
        self.bord.draw(*self.dr_inf, self.color)

        for j in to_dr:
            i = j[0]
            pos = i[1] * self.b_inf[2] + self.b_inf[0], \
                  i[0] * self.b_inf[2] + self.b_inf[1]
            s = pg.Surface((self.b_inf[2], self.b_inf[2]))
            s.set_alpha(150)
            s.fill(j[1])
            sc.blit(s, pos)

    def do_game(self):
        p = self.players[self.color]
        # print(p.select_pos)
        self.draw(p.draw())
        r = p.get_step(self.click_pos)
        # print(r)
        if r:
            print(1)
            self.bord.step(self.color, *r[0][::-1], *r[1][::-1])
            self.color *= -1
            f = self.bord.is_win(-self.color)
            if f:
                self.draw()
                return True

    def grit_pos(self, pos):
        return (pos[0] - self.b_inf[0]) // self.b_inf[2], (pos[1] - self.b_inf[1]) // self.b_inf[2]

    def click(self, pos):
        self.click_pos = pos
        if self.players[self.color].__class__ == PlayerP:
            self.players[self.color].click(*self.grit_pos(pos))


def load_image(name, colorkey=None):  # загружает картинки
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        exit(0)
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
    (King, 1): pg.transform.scale(load_image('f1.png'), (fig_sz, fig_sz)),
    (King, -1): pg.transform.scale(load_image('f7.png'), (fig_sz, fig_sz)),
    (Queen, 1): pg.transform.scale(load_image('f2.png'), (fig_sz, fig_sz)),
    (Queen, -1): pg.transform.scale(load_image('f8.png'), (fig_sz, fig_sz))
}

clock = pg.time.Clock()

font = pg.font.Font(None, 24)
font2 = pg.font.Font(None, 48)

pl = (PlayerAi, PlayerAi)

game = UiGame(sc, font, *bord_pos, fig_sz, pl)

while True:
    sc.fill(gray)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit(0)
        elif event.type == pg.MOUSEBUTTONDOWN:
            game.click(event.pos)

    # sc.blit(font.render(str(round(clock.get_fps())), False, red), (width - 50, 30))

    if game.do_game():
        t = f'Победил {"белый" if game.color == -1 else "чёрный"}'
        color = white if game.color == -1 else black
        sc.blit(font2.render(t, False, color), (width - font2.size(t)[0] - 50,
                                                height - font2.size(t)[1] - 10))
        pg.display.flip()
        f = True
        while f:
            if False:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        exit(0)
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        f = False
                        break
            else:
                sleep(1)
                break

        game = UiGame(sc, font, *bord_pos, fig_sz, pl)

    pg.display.flip()
    clock.tick(FPS)
