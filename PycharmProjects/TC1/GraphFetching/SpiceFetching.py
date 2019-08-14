from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PycharmProjects.TC1.GraphStructures.GraphValues import GraphValues, GraphTypes
from PycharmProjects.TC1.GraphStructures.ToggleableGraph import ToggleableGraph


class SpiceFetching(QDialog):
    def __init__(self, window, *args, **kwargs):
        super(SpiceFetching, self).__init__(*args, **kwargs)
        self.setWindowTitle("Searching File")
        self.setFixedSize(400, 300)
        self.file = ""
        self.window = window

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

    def spice_plot(self):
        self.file, _ = QFileDialog.getOpenFileName(self.window.parent, "Select LTSpice plots", "C://",
                                                "Bodes (*.txt)")
        if self.file:
            filename = self.file.split('/').pop()
            self.comment.setText("Escriba un nombre para el grafico de " + filename)
            self.show()

    def process_data(self):
        try:
            file = open(self.file, "r")
            if file.mode is not "r":
                print("ERROR")
                exit()
            lines = file.readlines()
            del lines[0]
            f = []
            amp = []
            phase = []
            for string in lines:
                freq, value = string.split()
                amp_, phase_ = value[1:-2].split(',')
                f.append(float(freq))
                amp.append(float(amp_[:-2]))
                phase.append(float(phase_))

            file.close()

            label = self.label.text()
            self.label.setText("")
            if label == "":
                label = "Graph " + str((len(self.window.graphicsToShow)+1))

            module_graph = ToggleableGraph(GraphValues(label, f, amp, GraphTypes.BodeModule),
                                           self.window.parent.spiceCheck.isChecked())
            self.window.add_graphic(module_graph, self.window.spiceKey)

            phase_graph = ToggleableGraph(GraphValues(label, f, phase, GraphTypes.BodePhase),
                                          self.window.parent.spiceCheck.isChecked())

            self.window.add_graphic(phase_graph, self.window.spiceKey)

            self.close()
            self.window.draw()

        except IOError:
            print("Not existing File")
            self.close()
        except ValueError:
            print("Invalid file format")
            self.close()
