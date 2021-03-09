from pprint import pprint
from copy import deepcopy
import numpy as np
import random as rnd


class NeuronNet:
    def __init__(self, layer_sizes=()):
        weight_shapes = [(a, b) for a, b in zip(layer_sizes[1:], layer_sizes[:-1])]
        self.weights = [np.random.standard_normal(s) / s[1] ** .5 for s in weight_shapes]
        self.biases = [np.zeros((s, 1)) for s in layer_sizes[1:]]

    def predict(self, a):
        for w, b in zip(self.weights, self.biases):
            a = self.activation(np.matmul(w, a) + b)
        # return a
        return [sum(i) / len(a) for i in a]
        # return [self.activation(sum(i)) for i in a]

    @staticmethod
    def activation(x):
        return 1 / (1 + np.exp(-x))

    def print(self):
        pprint(self.weights)
        print('\n\n' + '-' * 20 + '\n\n')
        pprint(self.biases)
        print('\n' * 4)

    def write(self):
        st = ''
        st += '\n\n'.join(['\n'.join([str(' '.join([str(h) for h in j])) for j in i]) for i in self.weights])
        st += '\n\n\n'
        b = [[str(j[0]) for j in i] for i in self.biases]
        for bb in range(len(b)):
            st += ' '.join([str(i) for i in b[bb]])
            st += '\n'
        return st

    @classmethod
    def read(cls, _r):
        _net = cls()
        wb = _r[:-1].split('\n\n\n')
        b = []
        for i in wb[1].split('\n'):
            b += [np.array([[float(j)] for j in i.split()])]
        _net.biases = deepcopy(b)

        w = []
        for i in wb[0].split('\n\n'):
            w += [[]]
            for j in i.split('\n'):
                w[-1] += [[float(h) for h in j.split()]]
        w = [np.array(i) for i in w]
        _net.weights = deepcopy(w)
        return _net


if __name__ == '__main__':
    net = NeuronNet((4, 30, 30, 30, 30, 100))
    # print(*net.predict((.01, .01)), sep='\n')

    # with open('net.net', 'w') as f:
    #     f.write(net.write())

    with open('net.net') as f:
        net2 = NeuronNet.read(f.read())

    a = [rnd.randrange(-100_000, 100_000) / 1000 for i in range(4)]

    pprint(net2.predict(a))
    pprint(max(enumerate(net2.predict(a)), key=lambda x: x[1])[0])











