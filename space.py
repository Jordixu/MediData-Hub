class Space():
    def __init__(self, number, floor, department, available):
        self.number = number
        self.floor = floor
        self.department = department
        self.available = available
        
    def is_available(self):
        return 'The room {self.number} is available' if self.available else 'The room {self.number} is not available'
    
    def make_available(self):
        self.available = True
    
    def make_unavailable(self):
        self.available = False
        
    def change_department(self, department):
        self.department = department
        
    def change_number(self, number):
        self.number = number