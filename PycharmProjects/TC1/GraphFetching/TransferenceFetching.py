from PycharmProjects.TC1.GraphStructures.GraphValues import GraphValues, GraphTypes
from PycharmProjects.TC1.GraphStructures.ToggleableGraph import ToggleableGraph

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from scipy import signal

from PycharmProjects.TC1.GraphStructures.GraphValues import GraphValues, GraphTypes
from PycharmProjects.TC1.GraphStructures.ToggleableGraph import ToggleableGraph


class TransferenceFetching(QWidget):
    def __init__(self, window, *args, **kwargs):
        super(TransferenceFetching, self).__init__(*args, **kwargs)
        loadUi('transfer.ui', self)
        self.user_inerfase = window
        self.finish.clicked.connect(self.analyzer)
        self.num_input.textChanged.connect(self.equation_draw)
        self.den_input.textChanged.connect(self.equation_draw)

    def transference_plot(self):
        self.show()

    def analyzer(self):
        numerator = self.num_input.text()
        denominator = self.den_input.text()
        """ Agarro los valores de los coeficientes"""
        coeficients_num = numerator.split(',')
        coeficients_den = denominator.split(',')
        try:
            num_coefs = [float(i) for i in coeficients_num]
            num_den = [float(i) for i in coeficients_den]
            transfer = signal.lti(num_coefs, num_den)
            freq, amp, phase = transfer.bode()
            label = self.labelName.text()
            self.labelName.setText("")
            if label == "":
                label = "Graph " + str((len(self.user_inerfase.graphicsToShow) + 1))
            graph_color = self.user_inerfase.get_next_color()
            module_graph = ToggleableGraph(GraphValues(label, freq, amp, GraphTypes.BodeModule),
                                           self.user_inerfase.parent.spiceCheck.isChecked())
            self.user_inerfase.add_graphic(module_graph, self.user_inerfase.spiceKey, graph_color)

            phase_graph = ToggleableGraph(GraphValues(label, freq, phase, GraphTypes.BodePhase),
                                          self.user_inerfase.parent.spiceCheck.isChecked())

            self.user_inerfase.add_graphic(phase_graph, self.user_inerfase.spiceKey, graph_color)

        except ValueError:
            print("not working")
            QMessageBox.warning(self, "Important", "Not numeric input",
                                        QMessageBox.Ok)

        self.close()
        self.equation.figure.clear()
        self.equation.canvas.draw()
        self.num_input.setText("")
        self.den_input.setText("")
        self.user_inerfase.draw()

    def equation_draw(self):
        self.equation.figure.clear()
        numerator = self.num_input.text()
        denominator = self.den_input.text()
        """ Agarro los valores de los coeficientes"""
        coeficients_num = numerator.split(',')
        coeficients_den = denominator.split(',')
        num_str = ""
        length = len(coeficients_num)
        for i in range(0, length):
            if (length - i) > 2:
                num_str += str(coeficients_num[i]) + ".s^" + str(length - 1 - i) + " + "
            elif (length - i) is 2:
                num_str += str(coeficients_num[i]) + ".s + "
            else:
                num_str += str(coeficients_num[i])
        if num_str == "":
            num_str = "-"
        den_str = ""
        length = len(coeficients_den)
        for i in range(0, length):
            if (length - i) > 2:
                den_str += str(coeficients_den[i]) + ".s^" + str(length - 1 - i) + " + "
            elif (length - i) is 2:
                den_str += str(coeficients_den[i]) + ".s + "
            else:
                den_str += str(coeficients_den[i])
        if den_str == "":
            den_str = "-"
        equation = "$ \\frac{"+num_str+"}{"+den_str+"}$"
        self.equation.figure.text(0, 0.5, equation, fontsize=10)
        self.equation.canvas.draw()
