from PyQt5.QtWidgets import QFileDialog

from PycharmProjects.TC1.GraphValues import GraphValues, GraphTypes
from PycharmProjects.TC1.ToggleableGraph import ToggleableGraph


class GraphManager:
    def __init__(self, mainWindow):
        self.graphicsToShow = {}
        self.parent = mainWindow
        self.transferenceKey = "transferenceKey"
        self.spiceKey = "spiceKey"
        self.medKey = "medKey"

    def add_graphic(self, graphic_value, key):

        if (len(self.graphicsToShow) == 0) or not (key in self.graphicsToShow.keys()) or \
                (self.graphicsToShow[key] is None) or (not isinstance(self.graphicsToShow[key], list)):
            self.graphicsToShow[key] = []
        self.graphicsToShow[key].append(graphic_value)

    def remove_graphic(self, key):
        self.graphicsToShow.pop(key)

    def remove_all_graphics(self):
        self.graphicsToShow.clear()
        self.draw()

    def __spice_button_graph__(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self.parent, "Select LTSpice plots", "C://",
                                                "Text Files (*.txt)")
        if files:
            data = self.__parse_ltspice_txt_file(files)
            for graph in data:
                module_graph = ToggleableGraph(GraphValues("Modulo", graph[0], graph[1], GraphTypes.BodeModule), True)
                phase_graph = ToggleableGraph(GraphValues("Fase", graph[0], graph[2], GraphTypes.BodePhase), True)
                self.add_graphic(module_graph,
                                 self.spiceKey)
                self.add_graphic(phase_graph, self.spicePhaseKey)

        self.draw()

    def __parse_ltspice_txt_file(self, files):
        try:
            data = []
            for filename in files:
                file = open(filename, "r")
                if file.mode is not "r":
                    print("ERROR")
                    exit()
                lines = file.readlines()
                del lines[0]
                f = []
                amp = []
                phase = []
                for string in lines:
                    frec, value = string.split()
                    amp_, phase_ = value[1:-2].split(',')
                    f.append(float(frec))
                    amp.append(float(amp_[:-2]))
                    phase.append(float(phase_))
                data.append((f, amp, phase))
                file.close()
            return data

        except IOError:
            print("File not found")
        except ValueError:
            print("Invalid file loaded")

    def __med_button_graph__(self):

        a = [22110, 345, 310, 28, 75, 2827, 120]
        b = [60, -70, 80, 90, 65, 87, 77]
        c = [10, 50, 564, 565, 5205, 5454, 222, 4000, 84444, 95512155, 578786786, 867867868768]
        d = [20, 45, -5434, 100, -24, 174, 788, 555, 800, 1050, 9999, 400]

        graphic5 = GraphValues("Bode Phase", c, d, GraphTypes.BodePhase)
        graphic4 = GraphValues("Bode Module", a, b, GraphTypes.BodeModule)
        self.add_graphic(ToggleableGraph(graphic4, True), self.medKey)
        self.add_graphic(ToggleableGraph(graphic5, True), self.medKey)
        self.draw()

    def __delete_button_graph__(self):
        self.remove_all_graphics()

    def draw(self):
        self.parent.graphics = list(self.graphicsToShow.values())
        self.parent.__update_graph__()

    def __trans_button_graph__(self):

        a = [10, 20, 30, 40, 75, 95, 120]
        b = [60, -70, 80, 90, 65, 88, 77]
        c = [10, 50, 80, 99, 120, 180, 222, 4000, 84444, 95555, 3333333, 5555555555555]
        d = [20, 45, -88, 100, -151, 174, 188, 555, 800, 1050, 9999, 400]

        graphic5 = GraphValues("Bode Phase", c, d, GraphTypes.BodePhase)
        graphic4 = GraphValues("Bode Module", a, b, GraphTypes.BodeModule)
        self.add_graphic(ToggleableGraph(graphic4, True), self.transferenceKey)
        self.add_graphic(ToggleableGraph(graphic5, True), self.transferenceKey)
        self.draw()

