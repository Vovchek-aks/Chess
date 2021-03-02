import numpy as np


class NeuronNet:
    def __init__(self, layer_sizes=()):
        weight_shapes = [(a, b) for a, b in zip(layer_sizes[1:], layer_sizes[:-1])]
        self.weights = [np.random.standard_normal(s) / s[1] ** .5 for s in weight_shapes]
        self.biases = [np.zeros((s, 1)) for s in layer_sizes[1:]]

    def predict(self, a):
        for w, b in zip(self.weights, self.biases):
            a = self.activation(np.matmul(w, a) + b)
        return [self.activation(sum(i)) for i in a]

    @staticmethod
    def activation(x):
        return 1 / (1 + np.exp(-x))

    @classmethod
    def open(cls, wb):
        n = cls()
        n.biases, n.weights = wb
        return n

    def print(self):
        print(*self.weights, sep='\n\n')
        print('\n\n' + '-' * 100 + '\n\n')
        print(*self.biases, sep='\n\n')

    def net(self):
        return self.biases, self.weights


if __name__ == '__main__':
    net = NeuronNet((2, 3, 3, 10))
    # print(*net.predict((.01, .01)), sep='\n')
    with open('net.txt', 'w') as f:
        f.write(str(net.net()))











