# Main class of the output window.
import os
from enum import Enum
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib as mpl
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from PycharmProjects.TC1.GraphManager import GraphManager
from PycharmProjects.TC1.GraphValues import GraphTypes


class UIWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("tcDesign.ui", self)
        self.setWindowTitle("Salida")
        self.graphics = None
        self.graphManager = GraphManager(self)
        self.transfButton.clicked.connect(self.graphManager.__trans_button_graph__)
        self.spiceButton.clicked.connect(self.graphManager.__spice_button_graph__)
        self.medButton.clicked.connect(self.graphManager.__med_button_graph__)
        self.deleteButton.clicked.connect(self.graphManager.__delete_button_graph__)
        self.changeLabels.clicked.connect(self.__label_edit__)
        self.exportButton.clicked.connect(self.__export_graphs__)
        self.ModuleWidget = self.graphwidget
        self.PhaseWidget = self.phaseGraph

        self.xLabel = "Eje x"
        self.yLabel = "Eje Y"

    def __export_graphs__(self):
        application_window = tk.Tk()
        application_window.withdraw()
        file_path = filedialog.askdirectory()


        moduleimage = self.__save_image__(file_path, self.ModuleWidget.figure, "module")
        phaseimage = self.__save_image__(file_path, self.PhaseWidget.figure, "phase")
        if not(messagebox.askokcancel("Selecciona", "¿Desea guardar las imagenes en archivos separados?")):
            new_image = self.concat_images(plt.imread(moduleimage)[:,:,:3], plt.imread(phaseimage)[:,:,:3])
            os.remove(moduleimage, phaseimage)
            self.__save_image__(file_path, new_image , "graphics" )

    def concat_images(self, imga, imgb):
        """
        Combines two color image ndarrays side-by-side.
        from https://stackoverflow.com/a/30228563/11331923
        """
        ha, wa = imga.shape[:2]
        hb, wb = imgb.shape[:2]
        max_height = np.max([ha, hb])
        total_width = wa + wb
        new_img = np.zeros(shape=(max_height, total_width, 3))
        new_img[:ha, :wa] = imga
        new_img[:hb, wa:wa + wb] = imgb
        return new_img

    def __save_image__(self, folder_path, image, name):
        i = 1
        if os.path.isfile(folder_path + "/" + name + ".png"):
            while os.path.isfile(folder_path + "/" + name + "(" + str(i) + ").png"):
                i = i + 1
            image.savefig(folder_path + "/" + name + "(" + str(i) + ").png")
            return folder_path + "/" + name + "(" + str(i) + ").png"
        else:
            image.savefig(folder_path + "/" + name + ".png")
            return folder_path + "/" + name + ".png"

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
        if self.graphics is not None:
            if len(self.graphics) > 0:
                for graphList in self.graphics:
                    for toggeable_graph in graphList:
                        if toggeable_graph.activated:
                            if toggeable_graph.graph.type == GraphTypes.BodeModule:
                                self.__plot_graph__(toggeable_graph.graph, self.ModuleWidget)
                            elif toggeable_graph.graph.type == GraphTypes.BodePhase:
                                self.__plot_graph__(toggeable_graph.graph, self.PhaseWidget)

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
        self.PhaseWidget.canvas.axes.annotate(y_title, xy=(0, 1), xytext=(-30, -ticklabelpad),
                                              ha='left', va='bottom',
                                              xycoords='axes fraction', textcoords='offset points', rotation=0)
        self.ModuleWidget.canvas.axes.annotate(y_title, xy=(0, 1), xytext=(-30, -ticklabelpad),
                                               ha='left', va='bottom',
                                               xycoords='axes fraction', textcoords='offset points', rotation=0)



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = UIWindow()
    window.show()
    app.exec()
