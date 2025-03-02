from foundation import Foundation
class Room(Foundation):
    """
    A class used to represent a room in a hospital.
    
    Attributes:
        number (int): The number of the room.
        floor (int): The floor of the room.
        department (str): The department the room is in.
        availability (dict): The availability of the room.
        
    Methods:
        get(attribute): Returns the value of the attribute.
        create_schedule(date, timeframes): Creates a schedule for the room.
        display_schedule(): Displays the schedule of the room.
        check_availability(date, timeframe): Checks the availability of the room.
        change_availability(date, timeframe): Changes the availability of the room.
        change_department(department): Changes the department of the room.
        change_number(number): Changes the number of the room.
        get_all_attributes(): Returns all the attributes
    """
    def __init__(self, number, floor, availability = None):
        self.__number = number # int
        self.__floor = floor # int
        self.__availability = availability if availability is not None else {}
    
    def display_schedule(self):
        return self.__availability
    
    def check_availability(self, date, timeframe):
        if date in self.__availability:
            if timeframe in self.__availability[date]:
                return self.__availability[date][timeframe]
        return False

    def change_availability(self, date, timeframe):
        if date in self.__availability and timeframe in self.__availability[date]:
            self.__availability[date][timeframe] = not self.__availability[date][timeframe]

        
    def change_number(self, number):
        previous_number = self.__number
        if self.__number == number:
            return f'The room number is already {self.__number}'
        self.__number = number
        return f'The room {previous_number} number is now {self.__number}'