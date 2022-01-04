from enum import Enum

# region Enums so user can enter only int without typing string
class damage_type_enum(Enum):
    Crack = 0
    Chip = 1
    Destroyed = 2

    # print string formatter
    @classmethod
    def print_all(cls):
        for i in location_enum:
            print("\t", i.name, " = ", i.value)


class hole_status_enum(Enum):
    In_Progress = 0
    Repaired = 1
    Not_Repaired = 2
    Temporary_Repair = 3


class location_enum(Enum):
    middle = 0
    curb = 1
    sidewalk = 2


# endregion Enums
