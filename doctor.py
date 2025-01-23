from person import Person
from notification import Notification

class Doctor(Person):
    def __init__(self, personal_id, password, name, surname, age, gender, speciality, department, socialsecurity, salary, hospital_id = None):
        super().__init__(personal_id, hospital_id, password, name, surname, age, gender)
        self._speciality = speciality
        self._department = department
        self._availability = {}
        self._socialsecurity = socialsecurity
        self._salary = salary
        self._assigned_patients = []
        self._notifications = []
        self._appointments = []
    
    def __str__(self):
        return f'Dr. {self.name} {self.surname}'
    
    def add_appointment(self, appointment):
        self._appointments.append(appointment)
        
    # def remove_last_appointment(self, appointment, last_appointment):
    #     if last_appointment:
    #         self._appointments.pop()
    #     elif not last_appointment:
    #         for app in self._appointments:
    #             if app == appointment:
    #                 self._appointments.remove(app)
                    
    def change_speciality(self, speciality):
        self._speciality = speciality
    
    def change_department(self, department):
        self._department = department
    
    def change_socialsecurity(self, socialsecurity):
        self._socialsecurity = socialsecurity
    
    def change_salary(self, salary):
        self._salary = salary
        
    def add_patient(self, patient):
        self._assigned_patients.append(patient)
        
    def remove_patient(self, patient, last_patient):
        if last_patient:
            self._assigned_patients.pop()
        elif not last_patient:
            for pat in self._assigned_patients:
                if pat == patient:
                    self._assigned_patients.remove(pat)
                    
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
