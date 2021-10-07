import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def dist(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def init_centroids(points, k):
    x_center = points['x'].mean()
    y_center = points['y'].mean()
    R = dist(x_center, y_center, points['x'][0], points['y'][0])
    for i in range(len(points)):
        R = max(R, dist(x_center, y_center, points['x'][i], points['y'][i]))
    x_c, y_c = [], []
    for i in range(k):
        x_c.append(x_center + R * np.cos(2 * np.pi * i / k))
        y_c.append(y_center + R * np.sin(2 * np.pi * i / k))
    return [x_c, y_c]


def nearest_centroid(x, y, centroids):
    r = float('inf')
    centroid_id = 0
    for i, (x_c, y_c) in enumerate(zip(centroids[0], centroids[1])):
        d = dist(x, y, x_c, y_c)
        if d < r:
            centroid_id = i
            r = d
    return centroid_id


def nearest_centroids(points, centroids):
    c_ids = []
    for i in range(len(points['x'])):
        c_ids.append(nearest_centroid(points['x'][i], points['y'][i], centroids))
    return c_ids


def recalculate_centroids(points, nearest_centroid_ids, centroids):
    x_c, y_c = [], []
    for i in range(len(centroids[0])):
        x_sum, y_sum, num = 0, 0, 0
        for j in range(len(points['x'])):
            if nearest_centroid_ids[j] == i:
                x_sum += points['x'][j]
                y_sum += points['y'][j]
                num += 1
        x_c.append(x_sum / max(num, 1))
        y_c.append(y_sum / max(num, 1))
    return [x_c, y_c]


def centroids_equal(old_centroids, new_centroids):
    for j in range(len(old_centroids)):
        for i in range(len(old_centroids[j])):
            if old_centroids[j][i] != new_centroids[j][i]:
                return False
    return True


def kmeans(points, k):
    centroids = init_centroids(points, k)
    nearest_centroid_ids = nearest_centroids(points, centroids)
    prev_centroids = centroids
    centroids = recalculate_centroids(points, nearest_centroid_ids, centroids)
    while not centroids_equal(prev_centroids, centroids):
        nearest_centroid_ids = nearest_centroids(points, centroids)
        prev_centroids = centroids
        centroids = recalculate_centroids(points, nearest_centroid_ids, centroids)
    return nearest_centroid_ids, centroids


def kmeans_step_draw(points, k):
    centroids = init_centroids(points, k)
    nearest_centroid_ids = nearest_centroids(points, centroids)
    step = 0
    draw(points, nearest_centroid_ids, k, centroids, 'optimal k = ' + str(k) + ', step ' + str(step))
    prev_centroids = centroids
    centroids = recalculate_centroids(points, nearest_centroid_ids, centroids)
    while not centroids_equal(prev_centroids, centroids):
        nearest_centroid_ids = nearest_centroids(points, centroids)
        prev_centroids = centroids
        step += 1
        draw(points, nearest_centroid_ids, k, centroids, 'optimal k = ' + str(k) + ', step ' + str(step))
        centroids = recalculate_centroids(points, nearest_centroid_ids, centroids)
    return nearest_centroid_ids, centroids


def draw(points, nearest_centroid_ids, k, centroids, title):
    colors = plt.get_cmap('gist_rainbow')
    for i in range(len(points['x'])):
        plt.scatter(points['x'][i], points['y'][i], color=colors(nearest_centroid_ids[i] / k))
    for i in range(k):
        plt.scatter(centroids[0][i], centroids[1][i], marker='x', color=colors(i / k), s=100, linewidths=2)
    plt.suptitle(title)
    plt.show()


def square_dist_sum(points, nearest_centroid_ids, centroids):
    sum = 0
    for i in range(len(points['x'])):
        sum += dist(points['x'][i], points['y'][i],
                    centroids[0][nearest_centroid_ids[i]], centroids[1][nearest_centroid_ids[i]]) \
               ** 2
    return sum


def d_k(j_prev, j, j_next):
    return abs(j - j_next) / abs(j_prev - j)


if __name__ == '__main__':
    filename = 'dataset.csv'
    n_points = 100
    max_k = 10
    points = pd.read_csv(filename)

    nearests, cents = kmeans(points, 1)
    prev = square_dist_sum(points, nearests, cents)
    draw(points, nearests, 1, cents, 'k = 1')

    nearests, cents = kmeans(points, 2)
    current = square_dist_sum(points, nearests, cents)
    draw(points, nearests, 2, cents, 'k = 2')

    deltas = []
    for i in range(3, max_k + 1):
        nearests, cents = kmeans(points, i)
        nextt = square_dist_sum(points, nearests, cents)
        draw(points, nearests, i, cents, 'k = ' + str(i))
        deltas.append(d_k(prev, current, nextt))
        prev, current = current, nextt
        print('k = ' + str(i - 1) + ', D(k) = ' + str(deltas[i - 3]))

    min_d_index = np.argmin(deltas)
    print(f'min D(k) = {deltas[min_d_index]}, best num of clusters = {min_d_index + 2}')
    kmeans_step_draw(points, min_d_index + 2)
