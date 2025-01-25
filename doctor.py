from person import Person
from notification import Notification
from datetime import date

class Doctor(Person):
    def __init__(self, 
            personal_id: int,
            hospital_id: int,
            password: str, 
            name: str, 
            surname: str, 
            birthday: date, 
            gender: str, 
            speciality: str, 
            department: str, 
            socialsecurity: str, 
            salary: float,  
            availability: dict = None, 
            assigned_patients: list = None, 
            notifications: list = None, 
            appointments: list = None
            ) -> None:
        
        super().__init__(personal_id, hospital_id, password, name, surname, birthday, gender, appointments)
        self.speciality = speciality
        self.department = department
        self.__availability = availability
        self.socialsecurity = socialsecurity
        self.salary = salary
        self.__assigned_patients = assigned_patients
        self.__notifications = notifications

    def __str__(self):
        return f'Dr. {self.name} {self.surname}'
                    
        
    def add_patient(self, patient):
        self.__assigned_patients.append(patient)
        
    def remove_patient(self, patient, last_patient):
        if last_patient:
            self.__assigned_patients.pop()
        elif not last_patient:
            for pat in self.__assigned_patients:
                if pat == patient:
                    self.__assigned_patients.remove(pat)
                    
    def create_schedule(self, date, timeframes):
        if date not in self.__availability:
            self.__availability[date] = {}
        for timeframe in timeframes:
            self.__availability[date][timeframe] = True
    
    def display_schedule(self):
        return self.__availability
    
    def check_availability(self, date, timeframe):
        if date in self.__availability:
            if timeframe in self.__availability[date]:
                return self.__availability[date][timeframe]
        return False
    
    def change_availability(self, date, timeframe):
        if date in self.__availability and timeframe in self.__availability[date]:
            self.__availability[date][timeframe] = not self.__availability[date][timeframe]
