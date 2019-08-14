import math
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PycharmProjects.TC1.GraphStructures.GraphValues import GraphValues, GraphTypes
from PycharmProjects.TC1.GraphStructures.ToggleableGraph import ToggleableGraph


class MeasurementFetching(QDialog):
    def __init__(self, mainWindow, *args, **kwargs):
        super(MeasurementFetching, self).__init__(*args, **kwargs)
        self.setWindowTitle("Searching File")
        self.setFixedSize(400, 300)
        self.file = ""
        self.window = mainWindow

        self.comment = QLabel(self)
        self.comment.setGeometry(QRect(50, 50, 300, 20))
        self.comment.setAlignment(Qt.AlignCenter | Qt.AlignTrailing | Qt.AlignVCenter)
        self.comment.setText("")

        self.label = QLineEdit(self)
        self.label.setGeometry(QRect(100, 150, 100, 20))
        self.label.setMaxLength(20)
        self.label.setText("")

        self.ok = QPushButton(self)
        self.ok.setGeometry(QRect(150, 250, 50, 20))
        self.ok.setText("Ok")
        self.ok.clicked.connect(self.process_data)

    def measurement_plot(self):
        boton = QMessageBox.warning(self.window.parent, "Important", "Format must be: Frequency | Vin | Vout", QMessageBox.Ok)
        if boton is QMessageBox.Ok:
            self.file, _ = QFileDialog.getOpenFileName(self.window.parent, "Select measured plots", "C://",
                                                    "Bodes (*.xls , *.xlsx , *.csv)")
            if self.file:
                filename = self.file.split('/').pop()
                self.comment.setText("Escriba un nombre para el grafico de " + filename)
                self.show()

    def process_data(self):
        try:
            raw_data = None
            file, extension = self.file.split('.')

            if extension == "xlsx" or extension == "xls":
                raw_data = pd.read_excel(self.file, header=None, skiprows=1)
            elif extension == "csv":
                raw_data = pd.read_csv(self.file, header=None, skiprows=1)

            if raw_data.shape[1] is not 3:
                raise ValueError

            f = []
            amp = []
            for i in range(0, len(raw_data)):
                f.append(float("{0:.1f}".format(raw_data[0][i])))
                _vin_vo_ = raw_data[2][i] / raw_data[1][i]
                amp.append(20 * math.log(_vin_vo_, 10))

            label = self.label.text()
            self.label.setText("")
            if label == "":
                label = "Graph " + str((len(self.window.graphicsToShow)+1))
            module_graph = ToggleableGraph(GraphValues(label, f, amp, GraphTypes.BodeModule),
                                           self.window.parent.spiceCheck.isChecked())
            self.window.add_graphic(module_graph, self.window.medKey)
            self.close()
            self.window.draw()
        except IOError:
            print("Not existing File")
            self.close()
        except ValueError:
            print("Invalid file format")
            self.close()
