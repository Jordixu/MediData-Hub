from person import Person
from notification import Notification

class Doctor(Person):
    def __init__(self, id, name, surname, age, gender, speciality, department, socialsecurity, salary):
        super().__init__(id, name, surname, age, gender, notifications = [])
        self.speciality = speciality
        self.department = department
        self.availability = {}
        self.socialsecurity = socialsecurity
        self.salary = salary
        self.assigned_patients = []
        
    def __str__(self):
        return f'Dr. {self.name} {self.surname}'
        
    def add_appointment(self, appointment):
        self.schedule.append(appointment)
    
    def remove_appointment(self, date, last_appointment):
        if last_appointment:
            self.schedule.pop()
        elif not last_appointment:
            for appointment in self.schedule:
                if appointment.date == date:
                    self.schedule.remove(appointment)
                    
    def change_speciality(self, speciality):
        self.speciality = speciality
    
    def change_department(self, department):
        self.department = department
    
    def change_socialsecurity(self, socialsecurity):
        self.socialsecurity = socialsecurity
    
    def change_salary(self, salary):
        self.salary = salary
        
    def add_patient(self, patient):
        self.assigned_patients.append(patient)
        
    def remove_patient(self, patient, last_patient):
        if last_patient:
            self.assigned_patients.pop()
        elif not last_patient:
            for pat in self.assigned_patients:
                if pat == patient:
                    self.assigned_patients.remove(pat)
                    
    def create_schedule(self, date, timeframes):
        if date not in self.availabilities:
            self.availabilities[date] = {}
        for timeframe in timeframes:
            self.availabilities[date][timeframe] = True
    
    def display_schedule(self):
        return self.availabilities