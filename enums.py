import enum
from enum import Enum


# region Enums so user can enter only int without typing string
class damage_type_enum(enum.Enum):
    Crack = 0
    Chip = 1
    Destroyed = 2

    # print string formatter
    @classmethod
    def print_all(cls):
        for i in location_enum:
            print("\t", i.name, " = ", i.value)

    def __str__(self):
        return str(self.value)


class hole_status_enum(enum.Enum):
    In_Progress = 0
    Repaired = 1
    Not_Repaired = 2
    Temporary_Repair = 3

    def __str__(self):
        return str(self.value)


class location_enum(enum.Enum):
    middle = 0
    curb = 1
    sidewalk = 2

    def __str__(self):
        return str(self.value)

# endregion Enums
