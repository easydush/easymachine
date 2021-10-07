import pandas as pd
from matplotlib import pyplot as plt
from numpy import recfromcsv
from pandas import read_csv


def show(data=[]):
    y = list(data['Date'])
    x = list(data['Monthly Mean Total Sunspot Number'])
    n = 20
    x_new = pd.DataFrame(x)
    x_new = x_new.rolling(window=n).mean()
    plt.plot(x_new, color='r')
    plt.figure(figsize=(50, 10))
    plt.scatter(y, x)
    plt.plot(y, x)
    plt.ylabel('Date')
    plt.xlabel('Sunspot')
    alpha = 0.5
    x_alpha = [x[0]]
    for n in range(1, len(x)):
        x_alpha.append(alpha*x[n] + (1-alpha)*x[n-1])
    plt.plot(y, x_alpha, color='g')
    plt.show()


def read_data(filename='data.csv'):
    return recfromcsv(filename, delimiter=',', encoding="UTF-8")


if __name__ == '__main__':
    filename = 'sunspots.csv'
    data = read_csv(filename)
    show(data)
