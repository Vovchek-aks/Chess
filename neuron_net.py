class Neuron:
    def __init__(self, func, weights):
        self.func = func
        self.weights = weights

    def get_result(self, inputs):
        out = self.func(sum(inputs))
        return [out * i for i in self.weights]

