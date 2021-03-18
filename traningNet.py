from chess import *
from neuron_net import NeuronNet


class TrGame:
    def __init__(self, nets):
        self.nets = nets
        self.bord = Bord()
        self.color = 1

    @classmethod
    def create(cls, cl, tp):
        return cls([NeuronNet(tp) for _ in range(cl)])

    @classmethod
    def open(cls, cl, name):
        return cls([NeuronNet.open(f'{name}{i}.net') for i in range(cl)])

    def save(self, name):
        for i in range(len(self.nets)):
            self.nets[i].save(f'{name}{i}.net')

    def print_nets(self):
        for i in self.nets:
            i.print()

    def bord_to_net(self):
        fg = (Pawn, King, Bishop, Rook, Queen, King)
        out = [0 for i in range(13*64)]
        for h in (1, -1):
            for i in range(6):
                for j in range(64):
                    f = self.bord[j]
                    if f.__class__ == fg[i] and f.color == h:
                        out[64*6*(h == -1) + i*64 + j] = 1
        return out


if __name__ == '__main__':
    # game = TrGame.create(64, (13*64, 64, 64, 2*64))
    # game.save('net')

    game = TrGame.open(1, 'net')
    game.print_nets()



    pass















