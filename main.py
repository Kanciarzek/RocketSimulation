import math
import sys
from math import sqrt
from PyQt5.QtWidgets import QWidget, QAction, QMessageBox, QInputDialog, QLineEdit, QLabel, QSlider, QPushButton, \
    QMenuBar, QMenu, QMainWindow, QApplication, QGridLayout
from qtconsole.qt import QtGui, QtCore
from scipy.integrate import odeint
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

    def __str__(self):
        return str(self.mass) + ',' + str(self.x) + ',' + str(self.y) + ',' + str(self.r)


class Globals:
    G = 6.61e-5
    angle = 0
    init_v = 0
    state = ""
    planets = [Planet(10000, 300, 50, 5), Planet(2000, 150, 100, 15)]


def parse_planets(string: str):
    planets = []
    for planet in string.split(';')[:-1]:
        args = planet.split(',')
        planets.append(Planet(float(args[0]), int(args[1]), int(args[2]), int(args[3])))
    return planets


def planets_to_string(planets: [Planet]):
    result = ""
    for planet in planets:
        result += str(planet) + ';'
    return result


def model(y, t, planets: [Planet]):
    posX, posY, vx, vy = y
    if any(planet.is_inside(posX, posY) for planet in planets):
        return [0, 0, -vx, -vy]
    res1 = sum(
        Globals.G * planet.mass * (planet.x - posX) / (sqrt((posX - planet.x) ** 2 + (posY - planet.y) ** 2)) ** 3 for
        planet in planets)
    res2 = sum(
        Globals.G * planet.mass * (planet.y - posY) / (sqrt((posX - planet.x) ** 2 + (posY - planet.y) ** 2)) ** 3 for
        planet in planets)
    return [vx, vy, res1, res2]


class ImageWidget(QWidget):
    def __init__(self, surface, parent=None):
        super(ImageWidget, self).__init__(parent)
        w = surface.get_width()
        h = surface.get_height()
        self.data = surface.get_buffer().raw
        self.image = QtGui.QImage(self.data, w, h, QtGui.QImage.Format_RGB32)

    def update(self, surface):
        w = surface.get_width()
        h = surface.get_height()
        self.data = surface.get_buffer().raw
        self.image = QtGui.QImage(self.data, w, h, QtGui.QImage.Format_RGB32)
        self.repaint()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.drawImage(0, 0, self.image)
        qp.end()


class Ui_RocketSimWindow(object):

    def velocity_change(self):
        Globals.init_v = self.horizontalSlider_2.value()
        self.label_2.setText("Prędkość początkowa: " + str(Globals.init_v))

    def angle_change(self):
        Globals.angle = self.horizontalSlider.value()
        self.label.setText("Kąt startu: " + str(Globals.angle))

    def wait(self):
        Globals.state = "wait"

    def restart(self):
        Globals.state = "restart"

    def quit(self):
        Globals.state = "quit"
        exit()

    def update_gravity(self):
        Globals.G = float(str(self.lineEdit.text()))

    def setupUi(self, RocketSimWindow, screen):
        RocketSimWindow.setObjectName("RocketSimWindow")
        RocketSimWindow.resize(518, 636)
        self.centralwidget = QWidget(RocketSimWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setText(str(Globals.G))
        self.lineEdit.textChanged.connect(self.update_gravity)
        self.gridLayout.addWidget(self.lineEdit, 5, 1, 1, 1)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.restart)
        self.gridLayout.addWidget(self.pushButton, 1, 2, 1, 1)
        self.graphicsView = ImageWidget(screen)
        self.graphicsView.setEnabled(True)
        self.graphicsView.setMouseTracking(False)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 3)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.horizontalSlider = QSlider(self.centralwidget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(180)
        self.horizontalSlider.valueChanged.connect(self.angle_change)
        self.gridLayout.addWidget(self.horizontalSlider, 3, 0, 1, 1)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.horizontalSlider_2 = QSlider(self.centralwidget)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.horizontalSlider_2.setMinimum(0)
        self.horizontalSlider_2.setMaximum(10)
        self.horizontalSlider_2.valueChanged.connect(self.velocity_change)
        self.gridLayout.addWidget(self.horizontalSlider_2, 3, 1, 1, 1)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.wait)
        self.gridLayout.addWidget(self.pushButton_2, 3, 2, 1, 1)
        RocketSimWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(RocketSimWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 518, 21))
        self.menubar.setObjectName("menubar")
        self.menuSymulacja = QMenu(self.menubar)
        self.menuSymulacja.setObjectName("menuSymulacja")
        self.menuEdytor_poziom_w = QMenu(self.menubar)
        self.menuEdytor_poziom_w.setObjectName("menuEdytor_poziom_w")
        RocketSimWindow.setMenuBar(self.menubar)
        self.actionSymulacja = QAction(RocketSimWindow)
        self.actionSymulacja.setObjectName("actionSymulacja")
        self.actionSymulacja.triggered.connect(ChangePlanetsWindow)
        self.actionEdytor_Poziom_w = QAction(RocketSimWindow)
        self.actionEdytor_Poziom_w.setEnabled(False)
        self.actionEdytor_Poziom_w.setObjectName("actionEdytor_Poziom_w")
        # self.actionWczytaj = QtWidgets.QAction(RocketSimWindow)
        # self.actionWczytaj.setObjectName("actionWczytaj")
        # self.actionZapisz = QtWidgets.QAction(RocketSimWindow)
        # self.actionZapisz.setObjectName("actionZapisz")
        self.actionWyj_cie = QAction(RocketSimWindow)
        self.actionWyj_cie.setObjectName("actionWyj_cie")
        self.actionWyj_cie.triggered.connect(self.quit)
        # self.menuSymulacja.addAction(self.actionZapisz)
        # self.menuSymulacja.addAction(self.actionWczytaj)
        self.menuSymulacja.addSeparator()
        self.menuSymulacja.addAction(self.actionWyj_cie)
        self.menuEdytor_poziom_w.addAction(self.actionSymulacja)
        self.menuEdytor_poziom_w.addAction(self.actionEdytor_Poziom_w)
        self.menubar.addAction(self.menuSymulacja.menuAction())
        self.menubar.addAction(self.menuEdytor_poziom_w.menuAction())
        oprogAct = QAction("O programie", self.centralwidget)
        oprogAct.triggered.connect(AboutWindow)
        self.menubar.addAction(oprogAct)

        self.retranslateUi(RocketSimWindow)
        QtCore.QMetaObject.connectSlotsByName(RocketSimWindow)

    def retranslateUi(self, RocketSimWindow):
        _translate = QtCore.QCoreApplication.translate
        RocketSimWindow.setWindowTitle(_translate("RocketSimWindow", "RocketSim"))
        self.pushButton.setText(_translate("RocketSimWindow", "Start"))
        self.label_3.setText(_translate("RocketSimWindow", "Stała grawitacji: "))
        self.label.setText(_translate("RocketSimWindow", "Kąt startu: " + str(Globals.angle)))
        self.label_2.setText(_translate("RocketSimWindow", "Prędkość początkowa: " + str(Globals.init_v)))
        self.pushButton_2.setText(_translate("RocketSimWindow", "Stop"))
        self.menuSymulacja.setTitle(_translate("RocketSimWindow", "Plik"))
        self.menuEdytor_poziom_w.setTitle(_translate("RocketSimWindow", "Edycja"))
        self.actionSymulacja.setText(_translate("RocketSimWindow", "Planety"))
        self.actionEdytor_Poziom_w.setText(_translate("RocketSimWindow", "---"))
        # self.actionWczytaj.setText(_translate("RocketSimWindow", "Wczytaj"))
        # self.actionZapisz.setText(_translate("RocketSimWindow", "Zapisz"))
        self.actionWyj_cie.setText(_translate("RocketSimWindow", "Wyjście"))


class ChangePlanetsWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        text, ok = QInputDialog.getText(self, 'Planety', 'Podaj planety:', QLineEdit.Normal,
                                        planets_to_string(Globals.planets))
        if ok:
            Globals.planets = parse_planets(str(text))


class AboutWindow(QWidget):

    def __init__(self):
        self.title = 'O programie'
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        QMessageBox.question(self, 'O programie',
                             'Autor: Paweł Goliszewski \nProjekt na przedmiot Modelowanie i Symulacja '
                             'Komputerowa \n2019', QMessageBox.Ok, QMessageBox.Ok)
        self.show()


class MainWindow(QMainWindow):
    def closeEvent(self, *args, **kwargs):
        Globals.state = "quit"
        super().closeEvent(*args, **kwargs)
        exit()


def main():
    pygame.init()
    screen = pygame.Surface((600, 500))
    app = QApplication(sys.argv)
    RocketSimWindow = MainWindow()
    ui = Ui_RocketSimWindow()
    ui.setupUi(RocketSimWindow, screen)
    RocketSimWindow.show()
    rocket = pygame.transform.scale(pygame.image.load('img/g3.png'), (32, 32))
    rocket_rect = rocket.get_rect()
    white = (255, 255, 255)
    black = (0, 0, 0)
    cur_time = 0
    clock = pygame.time.Clock()
    initx, inity = 0, 50
    points = []
    rotate_degree = Globals.angle
    max_time = 100000
    Globals.state = "wait"  # restart, wait, run, quit
    while Globals.state != "quit":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Globals.state = 'quit'
        screen.fill(white)
        if Globals.state == "restart":
            x = initx
            y = inity
            cur_time = 0
            # initial conditions
            y0 = [initx, inity, Globals.init_v * 0.05 * math.sin(math.radians(Globals.angle)),
                  - Globals.init_v * 0.05 * math.cos(math.radians(Globals.angle))]
            t = range(max_time)
            # solve ODE
            solution = odeint(model, y0, t, args=(Globals.planets,))
            Xs = solution[:, 0]
            Ys = solution[:, 1]
            points = []
            Globals.state = "run"
        elif Globals.state == "run":
            lastX = Xs[cur_time - 10]
            lastY = Ys[cur_time - 10]
            x = Xs[cur_time]
            y = Ys[cur_time]
            rotate_degree = math.degrees(math.atan((x - lastX) / (y - lastY))) if lastY - y != 0 else 0
            if lastY < y:
                rotate_degree += 180
            points.append((x, y))
            if len(points) > 1:
                pygame.draw.lines(screen, black, False, points)
            if cur_time + 10 >= max_time:
                points = []
            x = Xs[cur_time]
            y = Ys[cur_time]
            cur_time = (cur_time + 10) % max_time
        else:
            rotate_degree = -Globals.angle
            x = initx
            y = inity
        temp_rocket = pygame.transform.rotozoom(rocket, rotate_degree, 1)
        rocket_rect = temp_rocket.get_rect(center=rocket_rect.center)
        rocket_rect.centerx = x
        rocket_rect.centery = y
        for planet in Globals.planets:
            pygame.gfxdraw.aacircle(screen, planet.x, planet.y, planet.r, black)
        screen.blit(temp_rocket, rocket_rect)
        ui.graphicsView.update(screen)
        clock.tick(100)
    exit()


if __name__ == "__main__":
    main()
