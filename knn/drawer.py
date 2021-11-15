import pygame_widgets
import pygame
from pygame import KEYDOWN, K_ESCAPE
from sklearn.datasets import make_blobs

from knn import KNN
from utils import draw_button, draw_point, draw_points, Optimal

WIDTH = 1280
HEIGHT = 720
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KNN")
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
        self.clusters = 5
        self.init_data()
        self.current_k = 5
        self.optimal_k = Optimal(self.initial_points, self.initial_prediction)

    def init_data(self, amount=50):
        x_, y_ = make_blobs(n_samples=amount, centers=self.clusters,
                            cluster_std=40, center_box=(SURFACE - 50, HEIGHT - 50))
        self.points = list(map(lambda x: [x[0], x[1]], x_))
        self.prediction = list(map(lambda x: x + 1, y_))
        self.initial_points = self.points.copy()
        self.initial_prediction = self.prediction.copy()

    def draw_buttons(self, clusters=5):
        margin = 10
        width = 50
        height = 25
        for i in range(clusters):
            draw_button(screen, width * i + margin * i, 0, width, height, i + 1, on_click=self.on_click)
        draw_button(screen, width * clusters + margin * clusters, 0, width, height, 'start',
                    on_click=self.on_start)
        draw_button(screen, width * (clusters + 1) + margin * (clusters + 1), 0, width, height, 'restart',
                    on_click=self.on_restart)

    def draw_k_text(self, k):
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        text = f'Current k: {k}'
        text = font.render(text, True, LIGHT_GRAY)
        screen.blit(text, dest=(WIDTH / 2 - 150, 500))

    def on_click(self, text):
        if len(self.curr_point) > 0:
            self.optimal_k.get_optimal_k(self.curr_point, text)
            self.points.append(self.curr_point)
            self.prediction.append(text)
            self.curr_point = []
            screen.fill(BLACK)

    def on_start(self, text):
        self.curr_point = []
        screen.fill(BLACK)
        self.learning = False
        self.current_k = self.optimal_k.get_k()

    def on_restart(self, text):
        self.curr_point = []
        self.points = []
        screen.fill(BLACK)
        self.learning = True
        self.current_k = 5
        self.init_data()

    def start(self):
        done = False
        self.draw_buttons(self.clusters)

        while not done:
            clock.tick(FPS)
            events = pygame.event.get()
            pygame.draw.line(screen, BLACK, (0, SURFACE), (WIDTH, SURFACE))
            text = self.draw_k_text(self.current_k)
            for event in events:
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        done = True
                        exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pos()[1] > SURFACE:
                        self.curr_point = pygame.mouse.get_pos()
                        screen.fill(BLACK)
                        if self.learning:
                            draw_point(screen, pygame.mouse.get_pos(), RADIUS, GRAY)
                        else:
                            knn = KNN(self.current_k)
                            knn.fit(self.points, self.prediction)
                            pred = knn.predict([self.curr_point])
                            self.points.append(self.curr_point)
                            self.prediction += pred
                            self.curr_point = []

            pygame_widgets.update(events)
            pygame.display.update()

            if len(self.points) > 0:
                draw_points(screen, points_arr=self.points, clusters=self.prediction)
