class Room():
    def __init__(self, number, floor, department):
        self.number = number # int
        self.floor = floor # int
        self.department = department # string
        self.availability = {} # dictionary
    
    def create_schedule(self, date, timeframes):
        if date not in self.availabilities:
            self.availabilities[date] = {}
        for timeframe in timeframes:
            self.availabilities[date][timeframe] = True
    
    def display_schedule(self):
        return self.availabilities

    def change_department(self, department):
        if self.department == department:
            return f'The room {self.number} is already in the {self.department} department'
        self.department = department
        return f'The room {self.number} is now in the {self.department} department'
        
    def change_number(self, number):
        previous_number = self.number
        if self.number == number:
            return f'The room number is already {self.number}'
        self.number = number
        return f'The room {previous_number} number is now {self.number}'