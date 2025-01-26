from person import Person
from notification import Notification
from datetime import date

class Doctor(Person):
    """
    Represents a doctor in a hospital.
    
    Attributes:
        speciality (str): The speciality of the doctor.
        department (str): The department of the doctor.
        availability (dict): The availability of the doctor.
        assigned_patients (list): The list of patients assigned to the doctor.
        notifications (list): The list of notifications the doctor has received.
        salary (float): The salary of the doctor.
        socialsecurity (str): The social security number of the doctor.
    
    Methods:
        add_patient(patient_hid): Adds a patient to the doctor's list of assigned patients.
        remove_patient(patient_hid, last_patient): Removes a patient from the doctor's list of assigned patients.
        create_schedule(date, timeframes): Creates a schedule for the doctor.
        display_schedule(): Displays the doctor's schedule.
        check_availability(date, timeframe): Checks the availability of the doctor.
        change_availability(date, timeframe): Changes the availability of the doctor.
    """
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
            notification_id: list = None, 
            appointments: list = None
            ) -> None:
        
        super().__init__(personal_id, hospital_id, password, name, surname, birthday, gender, appointments)
        self.speciality = speciality
        self.department = department
        self.__availability = availability
        self.__socialsecurity = socialsecurity
        self.__salary = salary
        self.__assigned_patients = assigned_patients
        self.__notifications = notification_id

    def __str__(self):
        return f'Dr. {self.name} {self.surname}'
        
    def add_patient(self, patient_hid):
        self.__assigned_patients.append(patient_hid)
        
    def remove_patient(self, patient_hid, last_patient):
        if last_patient:
            self.__assigned_patients.remove(patient_hid)
        elif patient_hid in self.__assigned_patients:
            self.__assigned_patients.remove(patient_hid)
        else:
            return "Patient not found"
                    
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
            
    def get_all_attributes(self):
        attributes = self.__dict__
        attributes['availability'] = attributes.pop('_Doctor__availability')
        attributes['assigned_patients'] = attributes.pop('_Doctor__assigned_patients')
        attributes['notifications'] = attributes.pop('_Doctor__notifications')
        attributes['salary'] = attributes.pop('_Doctor__salary')
        attributes['socialsecurity'] = attributes.pop('_Doctor__socialsecurity')
        return attributes
