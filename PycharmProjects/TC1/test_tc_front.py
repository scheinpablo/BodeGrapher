# Main class of the output window.
from enum import Enum
import matplotlib as mpl
from PyQt5 import QtWidgets
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from graphwidget import GraphWidget


class GraphManager:
    def __init__(self):
        self.graphicToShow = {}
        self.transferenceModuleKey = "transferenceModule"
        self.spiceModuleKey = "spiceModule"
        self.medModuleKey = "measurementModule"
        self.transferencePhaseKey = "transferencePhase"
        self.spicePhaseKey = "spicePhase"
        self.medPhaseKey = "measeurementPhase"

    def add_graphic(self, graphic_value, key):
        self.graphicToShow[key] = graphic_value

    def remove_graphic(self, key):
        self.graphicToShow.pop(key)

    def remove_all_graphics(self):
        self.graphicToShow.clear()
        self.draw()

    def __spice_button_graph__(self):
        if (len(self.graphicToShow) > 0) and (self.spiceModuleKey in self.graphicToShow.keys()):
            self.remove_graphic(self.spiceModuleKey)
            self.remove_graphic(self.spicePhaseKey)
        else:
            i = 0
            self.draw()

    def __med_button_graph__(self):
        if (len(self.graphicToShow) > 0) and (self.medModuleKey in self.graphicToShow.keys()):
            self.remove_graphic(self.medModuleKey)
            self.remove_graphic(self.medPhaseKey)
            self.draw()
        else:
            a = [22110, 345, 310, 28, 75, 2827, 120]
            b = [60, -70, 80, 90, 65, 87, 77]
            c = [10, 50, 564, 565, 5205, 5454, 222, 4000, 84444, 95512155, 578786786, 867867868768]
            d = [20, 45, -5434, 100, -24, 174, 788, 555, 800, 1050, 9999, 400]
            e = [20, 20, 85, 85, -40, -280, 252]
            f = [60, -60, 80, -80, 64, 55, 22]

            graphic5 = GraphValues("Bode Phase", c, d, GraphTypes.BodePhase)
            graphic4 = GraphValues("Bode Module", a, b, GraphTypes.BodeModule)
            self.add_graphic(graphic4, self.medModuleKey)
            self.add_graphic(graphic5, self.medPhaseKey)
            self.draw()

    def __delete_button_graph__(self):
        self.remove_all_graphics()

    def draw(self):
        window.graphics = list(self.graphicToShow.values())
        window.__update_graph__()

    def __trans_button_graph__(self):
        if (len(self.graphicToShow) > 0) and (self.transferenceModuleKey in self.graphicToShow.keys()):
            self.remove_graphic(self.transferenceModuleKey)
            self.remove_graphic(self.transferencePhaseKey)
            self.draw()

        else:
            a = [10, 20, 30, 40, 75, 95, 120]
            b = [60, -70, 80, 90, 65, 88, 77]
            c = [10, 50, 80, 99, 120, 180, 222, 4000, 84444, 95555, 3333333, 5555555555555]
            d = [20, 45, -88, 100, -151, 174, 188, 555, 800, 1050, 9999, 400]
            e = [20, 20, 85, 85, -40, -280, 252]
            f = [60, -60, 80, -80, 64, 55, 22]

            graphic5 = GraphValues("Bode Phase", c, d, GraphTypes.BodePhase)
            graphic4 = GraphValues("Bode Module", a, b, GraphTypes.BodeModule)
            self.add_graphic(graphic4, self.transferenceModuleKey)
            self.add_graphic(graphic5, self.transferencePhaseKey)
            self.draw()


class OutputGraphics(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("tcDesign.ui", self)
        self.setWindowTitle("Salida")
        self.graphics = None
        self.graphManager = GraphManager()
        self.transfButton.clicked.connect(self.graphManager.__trans_button_graph__)
        self.spiceButton.clicked.connect(self.graphManager.__spice_button_graph__)
        self.medButton.clicked.connect(self.graphManager.__med_button_graph__)
        self.deleteButton.clicked.connect(self.graphManager.__delete_button_graph__)
        self.changeLabels.clicked.connect(self.__label_edit__)
        self.ModuleWidget = self.graphwidget
        self.PhaseWidget = self.phaseGraph

        self.xLabel = "Eje x"
        self.yLabel = "Eje Y"

    def __label_edit__(self):

        self.__fix_axes_titles_position__(self.xTextEdit.toPlainText(), self.yTextEdit.toPlainText())
        self.__update_graph__()
        self.xTextEdit.setPlainText(" ")
        self.yTextEdit.setPlainText(" ")

    def __update_graph__(self):
        self.ModuleWidget.canvas.axes.clear()
        self.PhaseWidget.canvas.axes.clear()

        self.PhaseWidget.canvas.draw()
        self.ModuleWidget.canvas.draw()
        if(self.graphics is not None):
            if len(self.graphics) > 0:
                for graph in self.graphics:
                    if graph.type == GraphTypes.BodeModule:
                        self.__plot_graph__(graph, self.ModuleWidget)
                    elif graph.type == GraphTypes.BodePhase:
                        self.__plot_graph__(graph, self.PhaseWidget)

        # draw each graph

    def __plot_graph__(self, graph, graph_widget):
        self.__fix_axes_titles_position__(self.xLabel, self.yLabel)
        graph_widget.canvas.axes.semilogx(graph.x_values,
                                          graph.y_values)
        graph_widget.canvas.axes.set_title(graph.title)
        graph_widget.canvas.axes.grid()
        graph_widget.canvas.draw()

    def __fix_axes_titles_position__(self, x_title, y_title):
        self.__fix_y_title_position__(y_title)
        self.__fix_x_title_position__(x_title)
        self.xLabel = x_title
        self.yLabel = y_title

    def __fix_x_title_position__(self, x_title):
        ticklabelpad = mpl.rcParams['xtick.major.pad']
        self.PhaseWidget.canvas.axes.annotate(x_title, xy=(1, 0), xytext=(0, -ticklabelpad),
                                              ha='left', va='top',
                                              xycoords='axes fraction', textcoords='offset points')
        self.ModuleWidget.canvas.axes.annotate(x_title, xy=(1, 0), xytext=(0, -ticklabelpad),
                                               ha='left', va='top',
                                               xycoords='axes fraction', textcoords='offset points')

    def __fix_y_title_position__(self, y_title):
        ticklabelpad = mpl.rcParams['ytick.major.pad']
        self.PhaseWidget.canvas.axes.annotate(y_title, xy=(0, 1), xytext=(-50, -ticklabelpad),
                                              ha='left', va='top',
                                              xycoords='axes fraction', textcoords='offset points', rotation=90)
        self.ModuleWidget.canvas.axes.annotate(y_title, xy=(0, 1), xytext=(-50, -ticklabelpad),
                                               ha='left', va='top',
                                               xycoords='axes fraction', textcoords='offset points', rotation=90)


# Testing Bench Class
class Out:
    @staticmethod
    def return_out():
        a = [10, 20, 30, 40, 75, 95, 120]
        b = [60, -70, 80, 90, 65, 88, 77]
        c = [10, 50, 80, 99, 120, 180, 222, 4000, 84444, 95555, 3333333, 5555555555555]
        d = [20, 45, -88, 100, -151, 174, 188, 555, 800, 1050, 9999, 400]
        e = [20, 20, 85, 85, -40, -280, 252]
        f = [60, -60, 80, -80, 64, 55, 22]

        graphic4 = GraphValues("Bode Phase", c, d, GraphTypes.BodePhase)
        graphic5 = GraphValues("Bode Module", a, b, GraphTypes.BodeModule)

        a = [graphic5, graphic4]
        return a


# Class GraphValues
# This class is used to unify the properties of the graphs to show.
class GraphValues:
    def __init__(self, title, x_value_array, y_value_array, graphic_type):
        self.title = title
        self.x_values = x_value_array
        self.y_values = y_value_array
        self.type = graphic_type


class GraphTypes(Enum):
    """ GraphTypes """
    BodeModule = "BodeModule"
    BodePhase = "BodePhase"


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = OutputGraphics()
    window.show()
    app.exec()
