# Main class of the output window.
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import cv2
import matplotlib as mpl
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from PycharmProjects.TC1.GraphStructures.GraphValues import GraphTypes
from PycharmProjects.TC1.ImageMananagent.ImageManagement import ImageManagement
from PycharmProjects.TC1.UIManagement.GraphManager import GraphManager


class UIWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('tcDesign.ui', self)
        self.setWindowTitle("Plot Tool")
        self.graphics = None
        self.graphManager = GraphManager(self)
        self.transfButton.clicked.connect(self.graphManager.trans_button_graph)
        self.spiceButton.clicked.connect(self.graphManager.spice_button_graph)
        self.medButton.clicked.connect(self.graphManager.med_button_graph)
        self.deleteButton.clicked.connect(self.delete_all)
        self.changeModuleLabels.clicked.connect(self.__label_module_edit__)
        self.changePhaseLabels.clicked.connect(self.__label_phase_edit__)
        self.spiceCheck.stateChanged.connect(self.graphManager.spice_checked)
        self.transferenceCheck.stateChanged.connect(self.graphManager.transf_checked)
        self.medCheck.stateChanged.connect(self.graphManager.med_checked)
        self.ModuleWidget = self.graphwidget
        self.PhaseWidget = self.phaseGraph
        self.ModuleWidget.canvas.axes.set_title('Module')
        self.PhaseWidget.canvas.axes.set_title('Phase')
        self.ModuleWidget.save_all_callback = self.export_graphs
        self.PhaseWidget.save_all_callback = self.export_graphs
        self.ModuleWidget.redraw_callback = self.__update_graph__
        self.PhaseWidget.redraw_callback = self.__update_graph__

    def delete_all(self):
        self.graphManager.delete_button_graph()
        self.ModuleWidget.clear_marked_points()
        self.PhaseWidget.clear_marked_points()
        self.__update_graph__()

    def export_graphs(self):
        application_window = tk.Tk()
        application_window.withdraw()
        file_path = filedialog.askdirectory()
        if file_path is not None and file_path != "":
            answer = messagebox.askyesnocancel(title="Selecciona",
                                               message="¿Desea guardar las imagenes en archivos separados?")
            moduleimage = ImageManagement.save_image(file_path, self.ModuleWidget.figure, "module")
            phaseimage = ImageManagement.save_image(file_path, self.PhaseWidget.figure, "phase")
            if not answer:
                im_v = ImageManagement.concat_images(moduleimage, phaseimage)
                name = ImageManagement.get_image_name(file_path, "signals")
                cv2.imwrite(name, im_v)
                os.remove(moduleimage)
                os.remove(phaseimage)

    def __label_module_edit__(self):
        self.ModuleWidget.x_label = self.xTextEdit.toPlainText()
        self.ModuleWidget.y_label = self.yTextEdit.toPlainText()
        self.__fix_axes_titles_position__(self.ModuleWidget)
        self.__update_graph__()
        self.xTextEdit.setPlainText(" ")
        self.yTextEdit.setPlainText(" ")

    def __label_phase_edit__(self):
        self.PhaseWidget.x_label = self.xTextEdit.toPlainText()
        self.PhaseWidget.y_label = self.yTextEdit.toPlainText()
        self.__fix_axes_titles_position__(self.PhaseWidget)
        self.__update_graph__()
        self.xTextEdit.setPlainText(" ")
        self.yTextEdit.setPlainText(" ")

    def __update_graph__(self):
        self.ModuleWidget.canvas.axes.clear()
        self.PhaseWidget.canvas.axes.clear()

        self.PhaseWidget.canvas.draw()
        self.ModuleWidget.canvas.draw()
        self.ModuleWidget.graph_labels = []
        self.PhaseWidget.graph_labels = []
        # draw each activated graph
        if self.graphics is not None:
            if len(self.graphics) > 0:
                for graphList in self.graphics:
                    for toggeable_graph in graphList:
                        if toggeable_graph[0].activated:
                            if toggeable_graph[0].graph.type == GraphTypes.BodeModule:
                                self.ModuleWidget.graph_labels.append(toggeable_graph[0].graph.title)
                                self.__plot_graph__(toggeable_graph[0].graph, self.ModuleWidget, toggeable_graph[1])
                            elif toggeable_graph[0].graph.type == GraphTypes.BodePhase:
                                self.PhaseWidget.graph_labels.append(toggeable_graph[0].graph.title)
                                self.__plot_graph__(toggeable_graph[0].graph, self.PhaseWidget, toggeable_graph[1])
        # draw each point

        self.__plot_points__(self.PhaseWidget)

        self.__plot_points__(self.ModuleWidget)

    def __plot_points__(self, graph_widget):
        for i in range(len(graph_widget.x_marked_points)):
            x_point = graph_widget.x_marked_points[i]
            y_point = graph_widget.y_marked_points[i]
            graph_widget.canvas.axes.plot(x_point,
                                          y_point, color='red',
                                          markersize=8, marker='x')

            if 10 > x_point > -10:
                x_text = str(round(x_point, 2))
            else:
                x_text = str(int(round(x_point)))

            if 10 > y_point > -10:
                y_text = str(round(y_point, 2))
            else:
                y_text = str(int(round(y_point)))

            graph_widget.canvas.axes.annotate("[" + x_text + "; " + y_text + "]"
                                              , (x_point, y_point))
        graph_widget.canvas.axes.grid(self)
        graph_widget.canvas.draw()

    def __plot_graph__(self, graph, graph_widget, color):
        self.__fix_axes_titles_position__(graph_widget)
        graph_widget.canvas.axes.semilogx(graph.x_values,
                                          graph.y_values,
                                          color=color)
        graph_widget.canvas.axes.legend(graph_widget.graph_labels, loc='best')

        self.ModuleWidget.canvas.axes.set_title('Module')
        self.PhaseWidget.canvas.axes.set_title('Phase')
        graph_widget.canvas.axes.grid(self)
        graph_widget.canvas.draw()

    def __fix_axes_titles_position__(self, widget):
        self.__fix_y_title_position__(widget)
        self.__fix_x_title_position__(widget)

    def __fix_x_title_position__(self, widget):
        ticklabelpad = mpl.rcParams['xtick.major.pad']
        widget.canvas.axes.annotate(widget.x_label, xy=(1, 0), xytext=(0, -ticklabelpad),
                                    ha='left', va='top',
                                    xycoords='axes fraction', textcoords='offset points')

    def __fix_y_title_position__(self, widget):
        ticklabelpad = mpl.rcParams['ytick.major.pad']
        widget.canvas.axes.annotate(widget.y_label, xy=(0, 1), xytext=(-30, -ticklabelpad),
                                    ha='left', va='bottom',
                                    xycoords='axes fraction', textcoords='offset points', rotation=0)
