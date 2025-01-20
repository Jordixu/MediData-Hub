from person import Person
from notification import Notification

class Patient(Person):
    def __init__(self, personal_id, password, name, surname, age, gender, weight, height, assigned_doctor = None, status = 'Outpatient', hospital_id = None):
        super().__init__(personal_id, hospital_id, password, name, surname, age, gender)
        self.weight = weight
        self.height = height
        self.assigned_doctor = assigned_doctor
        self.status = status # Inpatient, Outpatient, Emergency
        self.appointments = {}
        self.medications = []
        self.allergies = []
        self.diagnoses = []
        self.notifications = []
        
    def __str__(self):
        return f'Patient {self.name} {self.surname}'
        
    # def add_consult(self, consult):
    #     self.previous_consults.append(consult)
        
    # def remove_consult(self, date, last_consult):
    #     if last_consult:
    #         self.previous_consults.pop()
    #     elif not last_consult:    
    #         for consult in self.previous_consults:
    #             if consult.date == date:
    #                 self.previous_consults.remove(consult)
        
    def add_diagnosis(self, diagnostic):
        self.previous_diagnoses.append(diagnostic)
        
    def remove_diagnosis(self, date, last_diagnosis):
        if last_diagnosis:
            self.diagnoses.pop()
        elif not last_diagnosis:
            for diagnosis in self.diagnoses:
                if diagnosis.date == date:
                    self.diagnoses.remove(diagnosis)
        
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
        self.status = status