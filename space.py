class Space():
    def __init__(self, number, floor, department, available):
        self.number = number # int
        self.floor = floor # int
        self.department = department # string
        self.availability = {} # dictionary
        self.non_availability = {} # dictionary
        
    # def is_available(self):
    #     return f'The room {self.number} is available' if self.available else f'The room {self.number} is not available'
    
    # def make_available(self):
    #     if not self.available:
    #         self.available = True
    #         return f'The room {self.number} is now available'
    #     return f'The room {self.number} is already available'
    
    # def make_unavailable(self):
    #     if self.available:
    #         self.available = False
    #         return f'The room {self.number} is now unavailable'
    #     return f'The room {self.number} is already unavailable'
    
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