from person import Person
from notification import Notification

class Patient(Person):
    def __init__(self, id, name, surname, age, sex, weight, height, assigned_doctor, status):
        super().__init__(id, name, surname, age, sex, notifications = [])
        self.weight = weight
        self.height = height
        self.assigned_doctor = assigned_doctor
        self.status = status # CAMBIAR
        self.previous_consults = []
        self.previous_diagnostics = []
        self.medication = []
        self.allergies = []
        
    def __str__(self):
        return f'Patient {self.name} {self.surname}'
        
    def add_consult(self, consult):
        self.previous_consults.append(consult)
        
    def remove_consult(self, date, last_consult):
        if last_consult:
            self.previous_consults.pop()
        elif not last_consult:    
            for consult in self.previous_consults:
                if consult.date == date:
                    self.previous_consults.remove(consult)
        
    def add_diagnostic(self, diagnostic):
        self.previous_diagnostics.append(diagnostic)
        
    def remove_diagnostic(self, date, last_diagnostic):
        if last_diagnostic:
            self.previous_diagnostics.pop()
        elif not last_diagnostic:
            for diagnostic in self.previous_diagnostics:
                if diagnostic.date == date:
                    self.previous_diagnostics.remove(diagnostic)
        
    def add_medication(self, medication):
        self.medication.append(medication)
        
    def remove_medication(self, medication, last_medication):
        if last_medication:
            self.medication.pop()
        elif not last_medication:
            for med in self.medication:
                if med == medication:
                    self.medication.remove(med)
        
    def add_allergy(self, allergy):
        self.allergies.append(allergy)
        
    def remove_allergy(self, allergy, last_allergy):
        if last_allergy:
            self.allergies.pop()
        elif not last_allergy:
            for al in self.allergies:
                if al == allergy:
                    self.allergies.remove(al)
                    
    def change_weight(self, weight):
        self.weight = weight
    
    def change_height(self, height):
        self.height = height
        
    def change_assigned_doctor(self, doctor):
        self.assigned_doctor = doctor
        
    def change_status(self, status):
        # CAMBIAR ESTO
        self.status = status