import math
import pandas as pd
from PyQt5.QtWidgets import *

from PycharmProjects.TC1.GraphStructures.GraphValues import GraphValues, GraphTypes
from PycharmProjects.TC1.GraphStructures.ToggleableGraph import ToggleableGraph


class MeasurementFetching:
    @staticmethod
    def measurement_plot(window):

        QMessageBox.warning(window.parent, "Important", "Format must be: Frequency | Vin | Vout", QMessageBox.Ok)

        file, _ = QFileDialog.getOpenFileName(window.parent, "Select LTSpice plots", "C://",
                                                "Bodes (*.xls , *.xlsx , *.csv)")
        raw_data = None
        try:
            _, extension = file.split('.')
            if extension == "xlsx" or extension == "xls":
                raw_data = pd.read_excel(file, header=None, skiprows=1)
            elif extension == "csv":
                raw_data = pd.read_csv(file, header=None, skiprows=1)

            if raw_data.shape[1] is not 3:
                raise ValueError

            f = []
            amp = []
            for i in range(0, len(raw_data)):
                f.append(float("{0:.1f}".format(raw_data[0][i])))
                _vin_vo_ = raw_data[2][i]/raw_data[1][i]
                amp.append(20*math.log(_vin_vo_, 10))

            module_graph = ToggleableGraph(GraphValues("Modulo", f, amp, GraphTypes.BodeModule),
                                           window.parent.spiceCheck.isChecked())
            window.add_graphic(module_graph, window.medKey)

        except IOError:
            print("Not existing File")
        except ValueError:
            print("Invalid file format")
