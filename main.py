import math

from PyQt5 import QtWidgets
from math import sqrt
import numpy as np
import window
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import pygame
import pygame.gfxdraw


class Planet:
    def __init__(self, mass: float, x: int, y: int, r: int):
        self.mass = mass
        self.x = x
        self.y = y
        self.r = r

    def is_inside(self, x: float, y: float):
        return (x - self.x) ** 2 + (y - self.y) ** 2 < self.r ** 2


G = 6.61e-5


def model(y, t, planets: [Planet]):
    posX, posY, vx, vy = y
    if any(planet.is_inside(posX, posY) for planet in planets):
        return [0, 0, -vx, -vy]
    res1 = sum(
        G * planet.mass * (planet.x - posX) / (sqrt((posX - planet.x) ** 2 + (posY - planet.y) ** 2)) ** 3 for planet in
        planets)
    res2 = sum(
        G * planet.mass * (planet.y - posY) / (sqrt((posX - planet.x) ** 2 + (posY - planet.y) ** 2)) ** 3 for planet in
        planets)
    return [vx, vy, res1, res2]


def main():
    pygame.init()
    pygame.display.set_caption("Rocket simulation")
    screen = pygame.display.set_mode((500, 500))
    rocket = pygame.transform.scale(pygame.image.load('img/g3.png'), (32, 32))
    rocket_rect = rocket.get_rect()
    white = (255, 255, 255)
    black = (0, 0, 0)
    cur_time = 0
    clock = pygame.time.Clock()
    running = True

    # initial condition
    y0 = [0, 50, 0, 0]
    max_time = 100000
    t = np.linspace(0, max_time, num=max_time)
    planets = [Planet(10000, 300, 50, 5), Planet(2000, 150, 100, 5)]
    # solve ODE
    solution = odeint(model, y0, t, args=(planets,))
    Xs = solution[:, 0]
    Ys = solution[:, 1]

    points = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(white)
        lastX = Xs[cur_time - 20]
        lastY = Ys[cur_time - 20]
        x = Xs[cur_time]
        y = Ys[cur_time]
        rotate_degree = math.degrees(math.atan((x - lastX) / (y - lastY))) if lastY - y != 0 else 0
        if lastY < y:
            rotate_degree += 180
        points.append((x, y))
        if len(points) > 1:
            pygame.draw.lines(screen, black, False, points)
        temp_rocket = pygame.transform.rotozoom(rocket, rotate_degree, 1)
        rocket_rect = temp_rocket.get_rect(center=rocket_rect.center)
        rocket_rect.centerx = x
        rocket_rect.centery = y
        for planet in planets:
            pygame.gfxdraw.aacircle(screen, planet.x, planet.y, planet.r, black)
        screen.blit(temp_rocket, rocket_rect)
        if cur_time + 10 >= max_time:
            points = []
        cur_time = (cur_time + 10) % max_time
        pygame.display.update()
        clock.tick(100)


if __name__ == "__main__":
    main()

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     Dialog = QtWidgets.QDialog()
#     ui = window.Ui_RocketSimWindow()
#     ui.setupUi(Dialog)
#     Dialog.show()
#     sys.exit(app.exec_())
