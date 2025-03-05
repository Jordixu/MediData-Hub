from foundation import Foundation
from datetime import date
from typing import Union
class Person(Foundation):

    def __init__(self, personal_id: int, hospital_id: int, password: str, name: str, surname: str, 
                birthday: date, gender: str, diagnoses: list = None, prescriptions: list = None, 
                appointments: list = None, notifications: list = None):
        self._personal_id = personal_id
        self._hospital_id = hospital_id
        self._password = password
        self._name = name
        self._surname = surname
        self._birthday = birthday
        self._gender = gender
        
        # Ensure diagnoses is a list
        if diagnoses is None:
            self._diagnoses = []
        elif isinstance(diagnoses, list):
            self._diagnoses = diagnoses
        else:
            self._diagnoses = []  # Handle case where non-list is passed
        
        # Ensure prescriptions is a list
        if prescriptions is None:
            self._prescriptions = []
        elif isinstance(prescriptions, list):
            self._prescriptions = prescriptions
        else:
            self._prescriptions = []  # Handle case where non-list is passed
        
        # Ensure appointments is a list
        if appointments is None:
            self._appointments = []
        elif isinstance(appointments, list):
            self._appointments = appointments
        else:
            self._appointments = []  # Handle case where non-list is passed
        
        # Ensure notifications is a list
        if notifications is None:
            self._notifications = []
        elif isinstance(notifications, list):
            self._notifications = notifications
        else:
            self._notifications = []  # Handle case where non-list is passed
        
    def __name__(self) -> str:
        return self._name + ' ' + self._surname
    
    def check_password(self, password: Union[str, int]) -> bool:
        return str(self._password) == str(password)

    def add_notification(self, notification_id: int) -> None:
        # print("Notification type", type(notification_id), type(self._notifications), self._notifications)
        if self._notifications is None or type(self._notifications) != list:
            self._notifications = [notification_id]
        else:
            self._notifications.append(notification_id)

    def display_last_notification(self): # Unfinished
        return self._notifications[-1]
    
    def add_appointment(self, appointment_id: int): # Falta mirar si los appointments ya existen
        if self._appointments is None or type(self._appointments) != list:
            self._appointments = [appointment_id]
            return
        else:
            if appointment_id in self._appointments:
                raise ValueError("Appointment already exists")
            else:
                self._appointments.append(appointment_id)
                return
            
    def add_diagnosis(self, diagnosis_id) -> None:
        """Adds a diagnosis to the patient.
        
        Args:
            diagnosis_id (int): The diagnosis ID to add.
        """
        print(f"Type of _diagnoses: {type(self._diagnoses)}, Value: {self._diagnoses}")
        if diagnosis_id not in self._diagnoses:
            self._diagnoses.append(diagnosis_id)
        else:
            raise ValueError('Diagnosis already exists')
        
    def remove_diagnosis(self, diagnosis_id) -> None:
        """Removes a diagnosis from the patient.
        
        Args:
            diagnosis_id (int): The diagnosis ID to remove.
        """
        try:
            del self._diagnoses[diagnosis_id]
        except IndexError:
            print('Diagnosis not found')
        
    def add_prescription(self, prescription_id) -> None:
        if prescription_id not in self._prescriptions:
            self._prescriptions.append(prescription_id)
        else:
            raise ValueError('Prescription already exists')
        
    def remove_prescription(self, prescription_id) -> None:
        try:
            del self._prescriptions[prescription_id]
        except IndexError:
            print('Prescription not found')