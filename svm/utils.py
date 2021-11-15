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
