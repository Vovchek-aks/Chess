FIG_IM_ST = {}


class Figure:
    def __init__(self, x, y):
        self.pos = self.x, self.y = x, y
        self.is_ded = False

    def get_im_st(self):
        return FIG_IM_ST[self.__class__]

    def get_step_pos(self):
        return None

    def ded(self):
        self.is_ded = True


class Bord:
    pass


