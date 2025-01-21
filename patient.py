from person import Person
from notification import Notification
from doctor import Doctor

class Patient(Person):
    def __init__(self, personal_id: int, password: str, name: str, surname: str, age: int, gender: str, weight: float, height: float, assigned_doctor: Doctor = None, status: str = 'Outpatient', hospital_id: int = None) -> None:
        super().__init__(personal_id, hospital_id, password, name, surname, age, gender)
        self.weight = weight
        self.height = height
        self.assigned_doctor = assigned_doctor
        self.status = status # Inpatient, Outpatient, Emergency
        self._appointments = {}
        self.medications = []
        self.allergies = []
        self.diagnoses = []
        self.notifications = []
        
    def __str__(self):
        return f'Patient {self.name} {self.surname}'
        
    def add_appointment(self, appointment):
        self._appointments.append(appointment)
        
    def remove_last_appointment(self, appointment, last_appointment):
        if last_appointment:
            self._appointments.pop()
        elif not last_appointment:
            for app in self._appointments:
                if app == appointment:
                    self._appointments.remove(app)
        
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
        
    def change_assigned_doctor(self, doctor):
        self.assigned_doctor = doctor
        
    def change_status(self, status):
        self.status = status