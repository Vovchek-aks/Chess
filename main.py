class Figure:
    def __init__(self, x, y, color):
        self.pos = self.y, self.x = y, x
        self.is_ded = False
        self.color = color

    def get_im_st(self):
        return FIG_IM_ST.get((self.__class__, self.color), '@')

    def __str__(self):
        return str((self.__class__.__name__, self.pos, self.color))

    def __repr__(self):
        return self.get_im_st()

    def get_step_pos(self, bord):
        return set()

    def get_attack_pos(self, bord):
        return set()

    def go_pos(self, bord):
        return self.get_step_pos(bord) | self.get_attack_pos(bord)

    def ded(self):
        self.is_ded = True


class StepAttack(Figure):
    def get_attack_pos(self, bord):
        return self.get_step_pos(bord)


class EmptyF(StepAttack):
    def __init__(self, x, y, color=0):
        super().__init__(x, y, 0)

    def get_step_pos(self, bord):
        return set()


class Pawn(Figure):
    def get_step_pos(self, bord):
        r = {(self.x, self.y + self.color)[::-1]} & bord.b_get_free()
        if self.color == 1 and self.y == 1 or \
           self.color == -1 and self.y == 6:
            r |= {(self.x, self.y + self.color * 2)[::-1]} & bord.b_get_free()
        return r

    def get_attack_pos(self, bord):
        y = self.y + self.color
        return {(self.x - 1, y)[::-1],
                (self.x + 1, y)[::-1]} & bord.b_get_busy(self.color)


class Knight(StepAttack):
    def get_step_pos(self, bord):
        return {(self.x - 1, self.y - 2)[::-1],
                (self.x + 1, self.y - 2)[::-1],

                (self.x + 2, self.y - 1)[::-1],
                (self.x + 2, self.y + 1)[::-1],

                (self.x - 1, self.y + 2)[::-1],
                (self.x + 1, self.y + 2)[::-1],

                (self.x - 2, self.y - 1)[::-1],
                (self.x - 2, self.y + 1)[::-1]} & bord.b_get_all(self.color)


class Rook(StepAttack):
    def get_step_pos(self, bord):
        r = set()
        f = bord.b_get_free()
        b = bord.b_get_busy(self.color)
        ssum = lambda x, y, z: tuple([x[g] + y[g] * z for g in range(len(x))])
        for p in [[1, 0], [0, 1], [0, -1], [-1, 0]]:
            for i in range(8):
                s = ssum(self.pos, p, i + 1)
                if s in f:
                    r.add(s)
                elif s in b:
                    r.add(s)
                    break
                else:
                    break
        return r


class Bishop(StepAttack):
    def get_step_pos(self, bord):
        r = set()
        f = bord.b_get_free()
        b = bord.b_get_busy(self.color)
        ssum = lambda x, y, z: tuple([x[g] + y[g] * z for g in range(len(x))])
        for p in [[1, 1], [-1, 1], [1, -1], [-1, -1]]:
            for i in range(8):
                s = ssum(self.pos, p, i + 1)
                if s in f:
                    r.add(s)
                elif s in b:
                    r.add(s)
                    break
                else:
                    break
        return r


class Queen(StepAttack):
    def get_step_pos(self, bord):
        return Bishop(*self.pos[::-1], self.color).go_pos(bord) | Rook(*self.pos[::-1], self.color).go_pos(bord)


class King(StepAttack):
    def get_step_pos(self, bord):
        return set([(self.x + i, self.y + j)[::-1]
                    for i in range(-1, 2)
                    for j in range(-1, 2)
                    if (i, j) != (0, 0)]) & bord.b_get_all(self.color)


class Bord:
    def __init__(self):
        sp = [Rook, Knight, Bishop, King, Queen, Bishop, Knight, Rook]

        self.grid = [[sp[x](x, 0, 1) for x in range(len(sp))]] + \
                    [[Pawn(x, 1, 1) for x in range(8)]] + \
                    [[EmptyF(x, y) for x in range(8)] for y in range(2, 6)] + \
                    [[Pawn(x, 6, -1) for x in range(8)]] + \
                    [[sp[x](x, 7, -1) for x in range(len(sp))]]

    def __getitem__(self, item):
        r = []
        for i in self.grid:
            r += i
        return r[item]

    def b_get_free(self):
        r = set()
        for i in self:
            if not i.color:
                r.add(i.pos)
        return r

    def b_get_busy(self, color):
        r = set()
        for i in self:
            if i.color and i.color != color:
                r.add(i.pos)
        return r

    def b_get_all(self, color):
        return self.b_get_free() | self.b_get_busy(color)


FIG_IM_ST = {
    (Pawn, 1): '♟',
    (Pawn, -1): '♙',
    (Rook, 1): '♜',
    (Rook, -1): '♖',
    (Knight, 1): '♞',
    (Knight, -1): '♘',
    (Bishop, 1): '♝',
    (Bishop, -1): '♗',
    (King, 1): '♛',
    (King, -1): '♕',
    (Queen, 1): '♚',
    (Queen, -1): '♔',
    (EmptyF, 0): '-'
}


b = Bord()

g = b.grid[6][1].go_pos(b)

print(*[i.__repr__() for i in b])

# for i in range(8):
#     for j in range(8):
#         if (i, j) in g:
#             print('#', end='  ')
#         else:
#             print('-', end='  ')
#     print()

