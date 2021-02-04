class Neuron:
    def __init__(self, func, weights):
        self.func = func
        self.weights = weights

    def get_result(self, inputs):
        out = self.func(sum(inputs))
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


class NeuronNet:
    pass

