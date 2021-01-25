FIG_IM_ST = {}


class Figure:
    def __init__(self, x, y, color):
        self.pos = self.x, self.y = x, y
        self.is_ded = False
        self.color = color

    def get_im_st(self):
        return FIG_IM_ST[self.__class__]

    def get_step_pos(self, bord: set):
        return set()

    def get_attack_pos(self, bord: set):
        return set()

    def ded(self):
        self.is_ded = True


class StepAttack(Figure):
    def get_attack_pos(self, bord: set):
        return self.get_step_pos(bord)


class Pawn(Figure):
    def get_step_pos(self, bord: set):
        return {(self.x, self.y - self.color)} & bord

    def get_attack_pos(self, bord: set):
        y = self.get_step_pos(bord).pop()[1]
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
    pass



