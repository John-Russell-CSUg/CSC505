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

# region Classes
class Citizen:
    def __init__(self, name, address, phone_number):
        self.name = name
        self.address = address
        self.phone_number = phone_number

    def __str__(self):
        return "Citizen: ", self.name, self.address, self.phone_number

    @classmethod
    def from_input(cls):
        return cls(
            input('Name: '),
            input('Address: '),
            input('Phone: ')
        )


class Repair_Crew:
    Id = 1
    size = 1


class Pothole_Report:
    id = int()

    def __init__(self, street_address, size, location, damage_type):
        self.street_address = street_address
        self.size = size
        self.priority = size * 2
        self.location = location
        self.damage_type = damage_type


class Work_Order:
    Pothole_Report
    Repair_Crew
    equipment = ""
    hours = 0
    filler_material = 0
    cost = 0

    def __str__(self):
        return str("Damage Type ", Pothole_Report.damage_type, str(self.cost))


class Damage_File:
    Citizen
    Work_Order

    def __str__(self):
        return str(Citizen, Work_Order)


def create_damage_file(citizen_user, new_workorder):
    new_damage_file = Damage_File()
    new_damage_file.Citizen = citizen_user
    new_damage_file.Work_Order = new_workorder
    print(new_damage_file.Citizen.name, new_damage_file.Citizen.address, new_damage_file.Citizen.phone_number)
    print(damage_type_enum(int(new_damage_file.Work_Order.Pothole_Report.damage_type)))
    print(new_damage_file.Work_Order.cost)


def create_workorder(citizen_user, new_report):
    new_workorder = Work_Order()
    new_workorder.Pothole_Report = new_report
    new_workorder.equipment = "New Equipment"
    new_workorder.Repair_Crew = Repair_Crew()
    new_workorder.hours = 10
    new_workorder.filler_material = new_report.size * 10
    new_workorder.cost = int((new_workorder.hours * 10)) + int((new_workorder.filler_material * 5))
    create_damage_file(citizen_user, new_workorder)


def public_works_report(citizen_user, pothole_location, curb_location, pothole_damagetype,
                        pothole_damage_size):
    new_report = Pothole_Report(pothole_location, pothole_damage_size, curb_location, pothole_damagetype)
    new_report.id = 1
    create_workorder(citizen_user, new_report)


def citizen_report():
    print("Please Enter your info: ")
    citizen_user = Citizen.from_input()
    pothole_location = input('What street is the pothole located: ')
    print("What part of the street is the pothole located? ")
    print(damage_type_enum.print_all())
    curb_location = input(": ")
    for i in damage_type_enum:
        print("\t", i.name, " = ", i.value)
    pothole_damagetype = input(": ")
    pothole_damage_size = input('Pothole Size (1-10): ')

    print("public works has received your report")
    public_works_report(citizen_user, pothole_location, curb_location, pothole_damagetype, pothole_damage_size)


citizen_report()
