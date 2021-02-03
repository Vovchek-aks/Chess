import numpy as np


class NeuronNet:
    def __init__(self, input_num, neuron_num, learning_rate):  # констр.(кол-во входов, кол-во нейронов)
        # МАТРИЦА ВЕСОВ
        # Задаем матрицу весов как случайное от -0,5 до 0,5
        self.weights = (np.random.rand(neuron_num, input_num) - 0.5)
        # Задаем параметр скорости обучения
        self.lr = learning_rate

        pass

    # Метод обучения нейронной сети
    def train(self, inputs_list, targets_list):  # принимает (вх. список данных, ответы)
        # Преобразовать список входов в вертикальный массив. .T - транспонирование
        inputs_x = np.array(inputs_list, ndmin=2).T  # матрица числа
        targets_Y = np.array(targets_list, ndmin=2).T  # матрица ответов: какое это число

        # ВЫЧИСЛЕНИЕ СИГНАЛОВ
        # Вычислить сигналы в нейронах. Взвешенная сумма.
        x = np.dot(self.weights, inputs_x)  # dot - умножение матриц X = W*I = weights * inputs
        # Вычислить сигналы, выходящие из нейрона. Функция активации - сигмоида(x)
        y = 1 / (1 + np.exp(-x))

        # ВЫЧИСЛЕНИЕ ОШИБКИ
        #  Ошибка E = -(цель - фактическое значение)
        E = -(targets_Y - y)

        # ОБНОВЛЕНИЕ ВЕСОВ
        # Меняем веса по каждой связи
        self.weights -= self.lr * np.dot((E * y * (1.0 - y)), np.transpose(inputs_x))

        pass

    # Метод прогона тестовых значений
    def query(self, inputs_list):  # Принимает свой набор тестовых данных
        # Преобразовать список входов в вертикальный 2D массив.
        inputs_x = np.array(inputs_list, ndmin=2).T

        # Вычислить сигналы в нейронах. Взвешенная сумма.
        x = np.dot(self.weights, inputs_x)
        # Вычислить сигналы, выходящие из нейрона. Сигмоида(x)
        y = 1 / (1 + np.exp(-x))

        return y
