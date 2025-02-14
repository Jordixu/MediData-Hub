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
            notifications: list = None, 
            appointments: list = None
            ) -> None:
        """
        Creates a Doctor instance.
        
        Args:
            personal_id (int): The personal ID of the doctor.
            hospital_id (int): The hospital ID of the doctor.
            password (str): The password for the doctor's account.
            name (str): The first name of the doctor.
            surname (str): The surname of the doctor.
            birthday (date): The birth date of the doctor
        """
        super().__init__(personal_id, hospital_id, password, name, surname, birthday, gender, appointments, notifications)
        self.__speciality = speciality
        self.__department = department
        self.__availability = availability if availability is not None else {}
        self.__socialsecurity = socialsecurity
        self.__salary = salary
        self.__assigned_patients = assigned_patients if assigned_patients is not None else []
        
    def __name__(self):
        return 'Doctor' + super().__name__()

    def __str__(self): # Debbugins
        return f'Dr. {self._name} {self._surname}'
        
    def add_patient(self, patient_hid: int) -> None:
        """
        Adds a patient to the doctor's list of assigned patients.
        
        Args:
            patient_hid (int): The ID of the patient to be added.
        """
        if patient_hid not in self.__assigned_patients:
            self.__assigned_patients.append(patient_hid)
        
    def remove_patient(self, patient_hid: int, last_patient: int) -> None:
        """
        Removes a patient from the doctor's list of assigned patients.
        
        Args:
            patient_hid (int): The ID of the patient to be removed.
            last_patient (bool): True if the patient is the last one in the list.
        """
        if last_patient:
            self.__assigned_patients.remove(patient_hid)
        elif patient_hid in self.__assigned_patients:
            self.__assigned_patients.remove(patient_hid)
        else:
            return "Patient not found"
                    
    # def create_schedule(self, date, timeframes):
    #     if date not in self.__availability:
    #         self.__availability[date] = {}
    #     for timeframe in timeframes:
    #         self.__availability[date][timeframe] = True
    
    def display_schedule(self): # Unfinished
        return self.__availability
    
    def check_availability(self, date: date, timeframe: tuple) -> bool:
        """
        Checks if the doctor is available at a given date and timeframe
        
        Args:
            date (date): The date to check.
            timeframe (tuple): The timeframe to check.
            
        Returns:
            bool: True if the doctor is available, False otherwise.
        """
        if date in self.__availability:
            if timeframe in self.__availability[date]:
                return self.__availability[date][timeframe]
        return False
    
    def change_availability(self, date: date, timeframe: tuple) -> None:
        """
        Changes the availability of the doctor at a given date and timeframe
        
        Args:
            date (date): The date to change.
            timeframe (tuple): The timeframe
        """
        if date in self.__availability and timeframe in self.__availability[date]:
            self.__availability[date][timeframe] = not self.__availability[date][timeframe]
        
