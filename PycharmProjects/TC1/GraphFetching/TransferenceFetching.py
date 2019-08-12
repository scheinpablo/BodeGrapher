from PycharmProjects.TC1.GraphStructures.GraphValues import GraphValues, GraphTypes
from PycharmProjects.TC1.GraphStructures.ToggleableGraph import ToggleableGraph


class TransferenceFetching:
    @staticmethod
    def transference_plot(window):
        a = [10, 20, 300, 400, 750, 9500, 12000]
        b = [60, -70, 80, 90, 65, 88, 77]
        c = [10, 50, 80, 99, 120, 180, 222, 4000, 84444, 95555, 3333333, 5555555555555]
        d = [20, 45, -88, 100, -151, 174, 188, 555, 800, 1050, 9999, 400]

        graphic5 = GraphValues("Trans Phase", c, d, GraphTypes.BodePhase)
        graphic4 = GraphValues("Trans Module", a, b, GraphTypes.BodeModule)
        window.add_graphic(ToggleableGraph(graphic4, window.parent.transferenceCheck.isChecked()), window.transferenceKey)
        window.add_graphic(ToggleableGraph(graphic5, window.parent.transferenceCheck.isChecked()), window.transferenceKey)