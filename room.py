class Room():
    def __init__(self, number, floor, department):
        self.number = number # int
        self.floor = floor # int
        self.department = department # string
        self._availability = {} # dictionary
    
    def create_schedule(self, date, timeframes):
        if date not in self._availability:
            self._availability[date] = {}
        for timeframe in timeframes:
            self._availability[date][timeframe] = True
    
    def display_schedule(self):
        return self._availability
    
    def check_availability(self, date, timeframe):
        if date in self._availability:
            if timeframe in self._availability[date]:
                return self._availability[date][timeframe]
        return False

    def change_availability(self, date, timeframe):
        if date in self._availability and timeframe in self._availability[date]:
            self._availability[date][timeframe] = not self._availability[date][timeframe]

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