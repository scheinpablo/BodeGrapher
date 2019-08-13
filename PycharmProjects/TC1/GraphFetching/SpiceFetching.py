from PyQt5.QtWidgets import QFileDialog

from PycharmProjects.TC1.GraphStructures.GraphValues import GraphValues, GraphTypes
from PycharmProjects.TC1.GraphStructures.ToggleableGraph import ToggleableGraph


class SpiceFetching:
    @staticmethod
    def __parse_ltspice_txt_file__(files):
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
                    freq, value = string.split()
                    amp_, phase_ = value[1:-2].split(',')
                    f.append(float(freq))
                    amp.append(float(amp_[:-2]))
                    phase.append(float(phase_))
                data.append((f, amp, phase))
                file.close()
            return data

        except IOError:
            print("File not found")
        except ValueError:
            print("Invalid file loaded")

    @staticmethod
    def spice_plot(window):
        files, _ = QFileDialog.getOpenFileNames(window.parent, "Select LTSpice plots", "C://",
                                                "Text Files (*.txt)")
        if files:
            data = SpiceFetching.__parse_ltspice_txt_file__(files)
            for graph in data:
                module_graph = ToggleableGraph(GraphValues("Modulo", graph[0], graph[1], GraphTypes.BodeModule),
                                               window.parent.spiceCheck.isChecked())
                phase_graph = ToggleableGraph(GraphValues("Fase", graph[0], graph[2], GraphTypes.BodePhase),
                                              window.parent.spiceCheck.isChecked())
                window.add_graphic(module_graph, window.spiceKey)
                window.add_graphic(phase_graph, window.spiceKey)