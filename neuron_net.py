import numpy as np


class NeuronNet:
    def __init__(self, layer_sizes):
        weight_shapes = [(a, b) for a, b in zip(layer_sizes[1:], layer_sizes[:-1])]
        self.weights = [np.random.standard_normal(s) / s[1] ** .5 for s in weight_shapes]
        self.biases = [np.zeros((s, 1)) for s in layer_sizes[1:]]

    def predict(self, a):
        for w, b in zip(self.weights, self.biases):
            a = self.activation(np.matmul(w, a) + b)
        return a

    @staticmethod
    def activation(x):
        return 1 / (1 + np.exp(-x))


if __name__ == '__main__':
    net = NeuronNet((1, 3))
    print(net.predict((0.2,)))
