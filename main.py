FIG_IM_ST = {}


class Figure:
    def __init__(self, x, y, color):
        self.pos = self.x, self.y = x, y
        self.is_ded = False
        self.color = color

    def get_im_st(self):
        return FIG_IM_ST[self.__class__]

    def __str__(self):
        return str((self.__class__.__name__, self.pos, self.color))

    def __repr__(self):
        return self.__str__()

    def get_step_pos(self, bord: set):
        return set()

    def get_attack_pos(self, bord: set):
        return set()

    def ded(self):
        self.is_ded = True


class StepAttack(Figure):
    def get_attack_pos(self, bord: set):
        return self.get_step_pos(bord)


class EmptyF(StepAttack):
    def get_step_pos(self, bord: set):
        return set()


class Pawn(Figure):
    def get_step_pos(self, bord: set):
        return {(self.x, self.y + self.color)} & bord

    def get_attack_pos(self, bord: set):
        y = self.y + self.color
        return {(self.x - 1, y),
                (self.x + 1, y)} & bord


class Knight(StepAttack):
    def get_step_pos(self, bord: set):
        return {(self.x - 1, self.y - 2),
                (self.x + 1, self.y - 2),

                (self.x + 2, self.y - 1),
                (self.x + 2, self.y + 1),

                (self.x - 1, self.y + 2),
                (self.x + 1, self.y + 2),

                (self.x - 2, self.y - 1),
                (self.x - 2, self.y + 1)} & bord


class Rook(StepAttack):
    def get_step_pos(self, bord: set):
        return set([(self.x, self.y + i) for i in range(-7, 8) if i != 0] +
                   [(self.x + i, self.y) for i in range(-7, 8) if i != 0]) & bord


class Bishop(StepAttack):
    def get_step_pos(self, bord: set):
        return set([(self.x + i, self.y + i) for i in range(-7, 8) if i != 0] +
                   [(self.x + i, self.y - i) for i in range(-7, 8) if i != 0]) & bord


class Queen(StepAttack):
    def get_step_pos(self, bord: set):
        return Bishop(*self.pos, self.color).get_step_pos(bord) | Rook(*self.pos, self.color).get_step_pos(bord)


class King(StepAttack):
    def get_step_pos(self, bord: set):
        return set([(self.x + i, self.y + j)
                    for i in range(-1, 2)
                    for j in range(-1, 2)
                    if (i, j) != (0, 0)]) & bord


class Bord:
    def __init__(self):
        sp = [Rook, Knight, Bishop, King, Queen, Bishop, Knight, Rook]

        self.grid = [[sp[x](x, 0, 1) for x in range(len(sp))]] + \
                    [[Pawn(x, 1, 1) for x in range(8)]] + \
                    [[EmptyF(x, y, 0) for x in range(8)] for y in range(2, 6)] + \
                    [[Pawn(x, 6, -1) for x in range(8)]] + \
                    [[sp[x](x, 7, -1) for x in range(len(sp))]]







# print(*Bord().grid, sep='\n')
