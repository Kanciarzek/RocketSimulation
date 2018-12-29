from PyQt5 import QtWidgets
import window
from math import sqrt

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


class Planet:
    def __init__(self, mass: float, x: int, y: int, r: int):
        self.mass = mass
        self.x = x
        self.y = y
        self.r = r

    def is_inside(self, x: float, y: float):
        return (x - self.x) ** 2 + (y - self.y) ** 2 < self.r ** 2


G = 6.61e-5


# function that returns dy/dt
def model(y, t, planets: [Planet]):
    posX, posY, vx, vy = y
    if any(planet.is_inside(posX, posY) for planet in planets):
        return [0, 0, -vx, -vy]
    res1 = sum(
        G * planet.mass * (planet.x - posX) / (sqrt((posX - planet.x) ** 2 + (posY - planet.y) ** 2)) for planet in
        planets)
    res2 = sum(
        G * planet.mass * (planet.y - posY) / (sqrt((posX - planet.x) ** 2 + (posY - planet.y) ** 2)) for planet in
        planets)
    return [vx, vy, res1, res2]


# initial condition
y0 = [0, 0, 10, 0]

# time points
t = np.linspace(0, 2000, num=2000)

planets = [Planet(1000, 50, 50, 5), Planet(2000, 150, 100, 5)]

# solve ODE
solution = odeint(model, y0, t, args=(planets,))

# plot results
plt.plot(t, solution[:, 0])
plt.xlabel('time')
plt.ylabel('x(t)')
plt.show()

plt.plot(t, solution[:, 1])
plt.xlabel('time')
plt.ylabel('y(t)')
plt.show()

plt.plot(t, solution[:, 2])
plt.xlabel('time')
plt.ylabel('vx(t)')
plt.show()

plt.plot(t, solution[:, 3])
plt.xlabel('time')
plt.ylabel('vy(t)')
plt.show()

plt.plot(solution[:, 0], solution[:, 1])
fig = plt.gcf()
ax = fig.gca()
for planet in planets:
    ax.add_artist(plt.Circle((planet.x, planet.y), planet.r, color='r'))
plt.show()

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     Dialog = QtWidgets.QDialog()
#     ui = window.Ui_RocketSimWindow()
#     ui.setupUi(Dialog)
#     Dialog.show()
#     sys.exit(app.exec_())
