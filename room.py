class Room():
    def __init__(self, number, floor, department):
        self.__number = number # int
        self.__floor = floor # int
        self.__department = department # string
        self.__availability = {} # dictionary
    
    def create_schedule(self, date, timeframes):
        if date not in self.__availability:
            self.__availability[date] = {}
        for timeframe in timeframes:
            self.__availability[date][timeframe] = True
    
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

    def change_department(self, department):
        if self.__department == department:
            return f'The room {self.__number} is already in the {self.__department} department'
        self.__department = department
        return f'The room {self.__number} is now in the {self.__department} department'
        
    def change_number(self, number):
        previous_number = self.__number
        if self.__number == number:
            return f'The room number is already {self.__number}'
        self.__number = number
        return f'The room {previous_number} number is now {self.__number}'
    
    def get_all_attributes(self):
        return self.__dict__