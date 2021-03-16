from chess import *
from neuron_net import NeuronNet
from ui import Player


class TrGame:
    def __init__(self, nets):
        self.nets = nets
        self.bord = Bord()
        self.color = 1

    @classmethod
    def create(cls, cl, tp):
        return TrGame([NeuronNet(tp) for _ in range(cl)])

    @classmethod
    def open(cls, cl, name):
        return TrGame([NeuronNet.open(f'{name}{i}.net') for i in range(cl)])

    def save(self, name):
        return TrGame([self.nets[i].save(f'{name}{i}.net') for i in range(len(self.nets))])


if __name__ == '__main__':
    game = TrGame.create(16, (64, 32, 32, 128))
    game.save('net')














