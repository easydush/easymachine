import numpy as np
from matplotlib import pyplot as plt
from numpy import genfromtxt, recfromcsv


def show(females, males):
    labels = ['females', 'males']
    fig1, ax1 = plt.subplots()
    ax1.pie([females, males], labels=labels, autopct='%1.2f%%')
    plt.show()


def read_data(filename='test_data.csv'):
    data = recfromcsv(filename, delimiter=',', encoding="UTF-8", usecols=np.arange(2, 4))
    survived = [num for num in data.tolist() if num[0] == 1]
    females = len([num for num in survived if num[1] == 0])
    males = len(survived) - females
    print(females, males)
    return females, males


if __name__ == '__main__':
    filename = 'test_data.csv'
    females, males = read_data(filename)
    show(females, males)
