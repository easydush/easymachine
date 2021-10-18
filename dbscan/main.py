import pygame
import numpy as np
from pygame import KEYDOWN, K_ESCAPE
import pygame.freetype  # Import the freetype module.

from dbscan import dbscan

WIDTH = 1920
HEIGHT = 1080
FPS = 120

RADIUS = 15
BLACK = (10, 0, 77)
CYAN = (84, 224, 208)
WHITE = (255, 255, 255)
PINK = (255, 20, 147)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (47, 79, 79)
SKY_BLUE = (135, 206, 235)
COLORS = [WHITE, PINK, CYAN, BLUE, YELLOW, SKY_BLUE]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BLACK)
pygame.display.set_caption('DBSCAN')
clock = pygame.time.Clock()
points = []

font = pygame.font.Font(pygame.font.get_default_font(), 36)
text = 'Click anywhere'
text = font.render(text, True, YELLOW)
screen.blit(text, dest=(WIDTH / 2 - 150, 500))

eps = 40
min_points = 1


def get_color(num):
    if num < 6:
        return COLORS[num - 1]
    else:
        return DARK_GREEN


def draw_points(points_arr, clusters):
    screen.fill(BLACK)
    for point, cluster in zip(points_arr, clusters):
        pygame.draw.circle(screen, get_color(cluster), point, RADIUS)


done = False
while not done:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            exit()

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                done = True
                exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            points.append(pygame.mouse.get_pos())
            prediction = dbscan(np.array(points), eps, min_points)
            draw_points(points_arr=points, clusters=prediction)

    pygame.display.update()
