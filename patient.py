from person import Person

class Patient(Person):
    def __init__(self, id, name, surname)
        super().__init__(id, name, surname)
        self.medical_history = []
        self.appointments = []
        