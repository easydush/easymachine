from math import sqrt


def get_distance(point_1, point_2):
    distance = 0.0
    for i in range(len(point_1)):
        distance += (point_1[i] - point_2[i]) ** 2
    return sqrt(distance)


class KNN():
    def __init__(self, k):
        self.k = k
        self.x_train = []
        self.y_train = []

    def fit(self, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train

    def nearest_neighbors(self, test_sample):
        distances = []
        for i in range(len(self.x_train)):
            distances.append((self.y_train[i], get_distance(self.x_train[i], test_sample)))
        distances.sort(key=lambda x: x[1])
        neighbors = []
        for i in range(self.k):
            neighbors.append(distances[i][0])
        return neighbors

    def predict(self, test_set):
        predictions = []
        for test_sample in test_set:
            neighbors = self.nearest_neighbors(test_sample)
            labels = [sample for sample in neighbors]
            prediction = max(labels, key=labels.count)
            predictions.append(prediction)
        return predictions
