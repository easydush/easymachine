import pygame_widgets
from pygame_widgets.button import Button
import pygame
from sklearn.datasets import make_blobs

from svm import SVM
from utils import draw_point, draw_points, get_colour

WIDTH = 1280
HEIGHT = 720
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('support vectors method')
clock = pygame.time.Clock()
BLACK = (10, 0, 77)
CYAN = (84, 224, 208)
LIGHT_GRAY = (175, 175, 175)
GRAY = (125, 125, 125)

screen.fill(BLACK)

eps = 40
min_points = 1
RADIUS = 10
SURFACE = 100


class Drawer:
    def __init__(self):
        self.curr_point = []
        self.prediction = []
        self.points = []
        self.initial_points = []
        self.initial_prediction = []
        self.learning = True
        self.clusters = 2
        self.init_temp_data()
        self.support_vectors = []
        self.line_arr = []
        self.above_line_arr = []
        self.below_line_arr = []

    def create_colors(self, n):
        return list(pygame.color.THECOLORS.values())[:n + 1]

    def init_temp_data(self, amount=50):
        X, y_true = make_blobs(n_samples=amount, centers=self.clusters,
                               cluster_std=40, center_box=(SURFACE - 50, HEIGHT - 50))
        self.points = list(map(lambda x: [x[0], x[1]], X))
        self.initial_points = self.points.copy()
        self.prediction = list(map(lambda x: x + 1, y_true))
        self.initial_prediction = self.prediction.copy()

    @staticmethod
    def draw_lines(line_arr, color=CYAN):
        for line_idx in range(len(line_arr) - 1):
            pygame.draw.line(screen, color, line_arr[line_idx], line_arr[line_idx + 1], 5)

    @staticmethod
    def draw_button(left, top, width, height, text, on_click):
        button = Button(screen, left, top, width, height, text=str(text), borderThickness=2,
                        borderColour=get_colour(text),
                        colour=CYAN, onClick=on_click, hoverColour=LIGHT_GRAY, onClickParams=[text])
        return button

    def on_button_click(self, text):
        if len(self.curr_point) > 0:
            self.points.append(self.curr_point)
            self.prediction.append(text)
            self.curr_point = []
            screen.fill(BLACK)

    def on_start_click(self, text):
        self.curr_point = []
        screen.fill(BLACK)
        self.learning = False
        svm = SVM(C=1.0)
        svm.fit(self.points, self.prediction)
        self.support_vectors = svm.get_support_vectors()

        self.line_arr, self.below_line_arr, self.above_line_arr = svm.get_lines()

    def draw_buttons(self, amount_clusters: int = 5):
        y = 25
        margin = 10
        width = 50
        height = 50
        for i in range(amount_clusters):
            self.draw_button(width * i + margin * i, y, width, height, i + 1, on_click=self.on_button_click)
        self.draw_button(width * amount_clusters + margin * amount_clusters, y, width, height, 'Run',
                         on_click=self.on_start_click)
        self.draw_button(width * (amount_clusters + 1) + margin * (amount_clusters + 1), y, width, height, 'Rerun',
                         on_click=self.on_restart_click)

    def on_restart_click(self, text):
        self.curr_point = []
        self.points = []
        screen.fill(BLACK)
        self.learning = True
        self.init_temp_data()
        self.clear_lines()

    def clear_lines(self):
        self.support_vectors = []
        self.line_arr = []
        self.above_line_arr = []
        self.below_line_arr = []

    def run(self):
        done = False
        self.draw_buttons(self.clusters)

        while not done:
            clock.tick(FPS)
            events = pygame.event.get()
            pygame.draw.line(screen, BLACK, (0, SURFACE), (WIDTH, SURFACE))
            for event in events:
                if event.type == pygame.QUIT:
                    done = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pos()[1] > SURFACE:
                        self.curr_point = pygame.mouse.get_pos()
                        screen.fill(BLACK)
                        draw_point(screen, pygame.mouse.get_pos(), RADIUS, GRAY)
                        self.clear_lines()

            if len(self.support_vectors) > 0:
                draw_points(screen, self.support_vectors, [3] * len(self.support_vectors))

            if len(self.line_arr) > 0:
                self.draw_lines(self.line_arr)

            if len(self.below_line_arr) > 0:
                self.draw_lines(self.below_line_arr, LIGHT_GRAY)

            if len(self.above_line_arr) > 0:
                self.draw_lines(self.above_line_arr, LIGHT_GRAY)

            pygame_widgets.update(events)
            pygame.display.update()

            if len(self.points) > 0:
                draw_points(screen, points_arr=self.points, clusters=self.prediction)
