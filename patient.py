from person import Person

class Patient(Person):
    def __init__(self, id, name, surname, weight, height, assigned_doctor):
        super().__init__(id, name, surname)
        self.previous_consults = []
        self.previous_diagnostics = []
        self.weight = weight
        self.height = height
        self.assigned_doctor = assigned_doctor
        self.status = None
        self.medication = []
        self.allergies = []