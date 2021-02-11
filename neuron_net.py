import math


class Neuron:
    def __init__(self, func, weights):
        self.func = func
        self.weights = weights

    def get_result(self, inputt):
        out = self.func(inputt)
        return (out * i for i in self.weights)


class NeuronLayer:
    def __init__(self, neurons):
        self.neurons = neurons

    def get_result(self, inputs):
        inp = [0 for _ in range(len(self.neurons))]
        for i in inputs:
            for j in range(len(self.neurons)):
                inp[j] += i[j]

        return (self.neurons[i].get_result(inp[i]) for i in range(len(self.neurons)))

    def __repr__(self):
        return str(len(self.neurons))


class NeuronNet:
    def __init__(self, layers):
        self.layers = layers

    def get_result(self, values):
        for i in range(len(self.layers)):
            values = self.layers[i].get_result(values)
        return values

    def __repr__(self):
        return '\n'.join([i.__repr__() for i in self.layers])


def sigma(value):
    return (1 + math.e**(-value))**-1 * 2 - 1


def shift(value):
    return 1


def generator(net):
    nnet = []
    for i in net.split('\n\n'):
        g = []
        for j in i.split('\n'):
            g += [Neuron(sigma, [int(g) for g in j.split()])]
        nnet += [NeuronLayer(g)]
    return NeuronNet(nnet)


# net = '10 20 35\n' \
#        '2 45 6\n' \
#        '\n' \
#        '2 4\n' \
#        '7 8\n' \
#        '4 4'
#
# print(generator(net))

