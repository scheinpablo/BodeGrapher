from PycharmProjects.TC1.GraphFetching.SpiceFetching import SpiceFetching
from PycharmProjects.TC1.GraphFetching.MeasurementFetching import MeasurementFetching
from PycharmProjects.TC1.GraphFetching.TransferenceFetching import TransferenceFetching


class GraphManager:
    def __init__(self, mainWindow):
        self.graphicsToShow = {}
        self.parent = mainWindow
        self.transferenceKey = "transferenceKey"
        self.spiceKey = "spiceKey"
        self.medKey = "medKey"

    def spice_checked(self):
        self.__toggle_graphics__(self.spiceKey)

    def transf_checked(self):
        self.__toggle_graphics__(self.transferenceKey)

    def med_checked(self):
        self.__toggle_graphics__(self.medKey)

    def __toggle_graphics__(self, key):
        if (len(self.graphicsToShow) > 0) and (key in self.graphicsToShow.keys()):
            for graph in self.graphicsToShow[key]:
                graph.activated = not graph.activated

        self.draw()

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

    def delete_button_graph(self):
        self.remove_all_graphics()

    def draw(self):
        self.parent.graphics = list(self.graphicsToShow.values())
        self.parent.__update_graph__()

    def trans_button_graph(self):

        TransferenceFetching.transference_plot(self)
        self.draw()

    def med_button_graph(self):

        MeasurementFetching.measurement_plot(self)
        self.draw()

    def spice_button_graph(self):

        SpiceFetching.spice_plot(self)

        self.draw()
