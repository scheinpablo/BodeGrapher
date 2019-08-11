# Class GraphValues
# This class is used to unify the properties of the graphs to show.
from enum import Enum


class GraphValues:
    def __init__(self, title, x_value_array, y_value_array, graphic_type):
        self.title = title
        self.x_values = x_value_array
        self.y_values = y_value_array
        self.type = graphic_type


class GraphTypes(Enum):
    """ GraphTypes """
    BodeModule = "BodeModule"
    BodePhase = "BodePhase"