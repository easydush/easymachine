import numpy as np


def dbscan(points_data, eps, minimum_points):
    length = len(points_data)
    labels = [0] * length
    cluster_idx = 0

    for i in range(0, length):
        if not (labels[i] == 0):
            continue
        neighbour_points = range_query(points_data, i, eps)
        if len(neighbour_points) < minimum_points:
            labels[i] = -1
        else:
            cluster_idx += 1
            grow_cluster(points_data, labels, i, neighbour_points, cluster_idx, eps, minimum_points)

    return labels


def grow_cluster(points_data, labels, point_idx, neighbour_points, cluster_idx, eps, minimum_points):
    labels[point_idx] = cluster_idx
    i = 0
    while i < len(neighbour_points):
        point = neighbour_points[i]
        if labels[point] == -1:
            labels[point] = cluster_idx

        elif labels[point] == 0:
            labels[point] = cluster_idx
            point_neighbour_points = range_query(points_data, point, eps)
            if len(point_neighbour_points) >= minimum_points:
                neighbour_points = neighbour_points + point_neighbour_points
        i += 1


def range_query(points_data, idx, eps):
    neighbours = []

    for point_idx in range(0, len(points_data)):
        if np.sqrt((points_data[idx][0] - points_data[point_idx][0]) ** 2 + (
                points_data[idx][1] - points_data[point_idx][1]) ** 2) < eps:
            neighbours.append(point_idx)
    return neighbours
