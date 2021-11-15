from math import sqrt

import numpy as np
import pygame
from pygame_widgets.button import Button

BLACK = (10, 0, 77)
WHITE = (255, 255, 255)
CYAN = (84, 224, 208)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (125, 125, 125)
LIGHT_GRAY = (175, 175, 175)
SKY_BLUE = (135, 206, 235)
PINK = (255, 20, 147)
DARK_GREEN = (47, 79, 79)
COLORS = [WHITE, PINK, CYAN, BLUE, YELLOW, SKY_BLUE]

RADIUS = 10


def get_colour(num):
    if isinstance(num, int) and num < 7:
        return COLORS[num - 1]
    else:
        return DARK_GREEN


def draw_point(screen, pos, radius, color):
    pygame.draw.circle(screen, color, pos, radius)


def draw_points(screen, points_arr, clusters):
    for point, cluster in zip(points_arr, clusters):
        draw_point(screen, point, RADIUS, get_colour(int(cluster)))


def draw_button(screen, left, top, width, height, text, on_click):
    button = Button(screen, left, top, width, height, text=str(text), borderThickness=1,
                    borderColour=get_colour(text),
                    colour=CYAN, onClick=on_click, hoverColour=LIGHT_GRAY, onClickParams=[text])
    return button


def get_distance(point_1, point_2):
    distance = 0.0
    for i in range(len(point_1)):
        distance += (point_1[i] - point_2[i]) ** 2
    return sqrt(distance)


class Optimal:

    def __init__(self, points, predictions):
        self.matrix = []
        self.points = points
        self.predictions = predictions

    def get_optimal_k(self, new_point, new_prediction):
        curr_dist_list = []
        for point, prediction in zip(self.points, self.predictions):
            curr_distance = get_distance(point, new_point)
            curr_dist_list.append((curr_distance, point, prediction))

        curr_dist_list.sort(key=lambda x: x[0])

        first_idx = -1
        res_arr = []
        for point_idx in range(len(curr_dist_list)):
            if curr_dist_list[point_idx][2] == new_prediction:
                first_idx = point_idx + 1
                res_arr.append(1)
            else:
                res_arr.append(0)
        print(res_arr)
        self.matrix.append(res_arr)

    def get_k(self):
        if len(self.matrix) == 0:
            return 5

        result_array = [0] * len(self.points)

        for res in self.matrix:
            for point in range(len(res)):
                result_array[point] += res[point]
        max_idx = np.argmax(result_array)
        return max_idx
