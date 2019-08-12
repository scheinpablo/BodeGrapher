# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class GraphWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.x_label = "Eje X"
        self.y_label = "Eje Y"
        self.figure = Figure(tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        vertical_layout = QVBoxLayout()

        self.toolbar.addAction(QIcon("Resources\saveall.png"), "Guardar ambos gráficos", self.save_all_pressed)
        self.toolbar.addAction(QIcon("Resources\mark.png"), "Marcar puntos", self.mark_points)

        a = self.toolbar._actions.keys()

        self.cid = self.figure.canvas.mpl_connect('button_press_event', self)

        vertical_layout.addWidget(self.canvas)
        vertical_layout.addWidget(self.toolbar)
        self.graph_labels = []
        self.x_marked_points = []
        self.y_marked_points = []
        self.canvas.axes = self.canvas.figure.add_subplot(111)

        self.setLayout(vertical_layout)
        self.save_all_callback = None
        self.redraw_callback = None

        self.mark_points_flag = False

    def __call__(self, event):
        if self.mark_points_flag:
            self.x_marked_points.append(event.xdata)
            self.y_marked_points.append(event.ydata)
            self.redraw_callback()

    def save_all_pressed(self):
        self.save_all_callback()

    def mark_points(self):
        self.mark_points_flag = not self.mark_points_flag
