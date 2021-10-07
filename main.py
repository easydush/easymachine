import numpy as np
from matplotlib import pyplot as plt
from numpy import genfromtxt, recfromcsv


def show(data=[]):
    y_pos = np.arange(1, len(data) + 1)
    plt.bar(y_pos, [x[1] for x in data], align='center', alpha=0.5,
            color=['red' if x[0] == 'f' else 'blue' for x in data])
    plt.xticks(y_pos)
    plt.ylabel('Age')

    plt.show()


def read_data(filename='data.csv'):
    return recfromcsv(filename, delimiter=',', encoding="UTF-8")


if __name__ == '__main__':
    filename = 'data.csv'
    data = read_data(filename)
    show(data)
