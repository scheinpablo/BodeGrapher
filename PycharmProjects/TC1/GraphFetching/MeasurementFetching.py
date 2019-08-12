from PycharmProjects.TC1.GraphStructures.GraphValues import GraphValues, GraphTypes
from PycharmProjects.TC1.GraphStructures.ToggleableGraph import ToggleableGraph


class MeasurementFetching:
    @staticmethod
    def measurement_plot(window):
        a = [50, 310, 345, 550, 750, 2827, 12000]
        b = [60, -70, 80, 90, 65, 87, 77]
        c = [10, 50, 564, 565, 5205, 5454, 6000, 40000, 84444, 95512155, 578786786, 867867868768]
        d = [20, 45, -5434, 100, -24, 174, 788, 555, 800, 1050, 9999, 400]

        graphic5 = GraphValues("Med Phase", c, d, GraphTypes.BodePhase)
        graphic4 = GraphValues("Med Module", a, b, GraphTypes.BodeModule)
        window.add_graphic(ToggleableGraph(graphic4, window.parent.medCheck.isChecked()), window.medKey)
        window.add_graphic(ToggleableGraph(graphic5, window.parent.medCheck.isChecked()), window.medKey)