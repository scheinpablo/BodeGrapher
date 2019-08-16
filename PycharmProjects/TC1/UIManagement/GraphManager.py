from PycharmProjects.TC1.GraphFetching.MeasurementFetching import MeasurementFetching
from PycharmProjects.TC1.GraphFetching.SpiceFetching import SpiceFetching
from PycharmProjects.TC1.GraphFetching.TransferenceFetching import TransferenceFetching


class GraphManager:
    def __init__(self, mainWindow):
        self.graphicsToShow = {}
        self.parent = mainWindow
        self.transferenceKey = "transferenceKey"
        self.spiceKey = "spiceKey"
        self.medKey = "medKey"
        self.measure = MeasurementFetching(self)
        self.spice = SpiceFetching(self)
        self.transfer = TransferenceFetching(self)
        self.colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    def spice_checked(self):
        self.__toggle_graphics__(self.spiceKey)

    def transf_checked(self):
        self.__toggle_graphics__(self.transferenceKey)

    def med_checked(self):
        self.__toggle_graphics__(self.medKey)

    def __toggle_graphics__(self, key):
        if (len(self.graphicsToShow) > 0) and (key in self.graphicsToShow.keys()):
            for graph in self.graphicsToShow[key]:
                graph[0].activated = not graph[0].activated

        self.draw()

    def add_graphic(self, graphic_value, key, color):

        if (len(self.graphicsToShow) == 0) or not (key in self.graphicsToShow.keys()) or \
                (self.graphicsToShow[key] is None) or (not isinstance(self.graphicsToShow[key], list)):
            self.graphicsToShow[key] = []
        self.graphicsToShow[key].append((graphic_value, color))

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

        self.transfer.transference_plot()

    def med_button_graph(self):

        self.measure.measurement_plot()

    def spice_button_graph(self):

        self.spice.spice_plot()

    def get_next_color(self):
        self.colors.reverse()
        next_color = self.colors.pop()
        self.colors.reverse()
        self.colors.append(next_color)
        return next_color
