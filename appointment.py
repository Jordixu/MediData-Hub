from datetime import date, time, datetime
from foundation import Foundation
import numpy as np

class Appointment(Foundation):
    """
    Represents an appointment in a hospital.
    
    Attributes:
        appointment_id (int): The ID of the appointment.
        date (date): The date of the appointment.
        timeframe (tuple): The time slot for the appointment (start_time, end_time).
        doctor_hid (int): The ID of the doctor assigned to the appointment.
        patient_hid (int): The ID of the patient scheduled for the appointment.
        room_number (int): The number of the room assigned for the appointment.
        status (str): The current status of the appointment.
        diagnosis_id (str): The diagnosis ID of the patient.
        medication_id (str): The medication ID prescribed to the patient.
        
    Methods:
        change_status(status): Changes the status of the appointment.
        autocomplete(): Automatically changes the status of the appointment to completed if the date and time have passed.
        change_datetime(date, timeframe): Changes the date and time of the appointment.
        change_doctor(doctor_hid): Changes the doctor assigned to the appointment.
    """
    def __init__(self, appointment_id: int, date: date, timeframe: tuple, doctor_hid: int, patient_hid: int, status: str, room_number: int = None, diagnosis_id: int = None, medication_id: int = None) -> None:
        """
        Initialize an Appointment instance.
        
        Args:
            appointment_id (int): The ID of the appointment.
            date (date): The date of the appointment.
            timeframe (tuple): The time slot for the appointment (start_time, end_time).
            doctor_hid (int): The ID of the doctor assigned to the appointment.
            patient_hid (int): The ID of the patient scheduled for the appointment.
            room_number (int): The number of the room assigned for the appointment.
            status (str): The current status of the appointment.
            diagnosis_id (int, optional): The diagnosis ID of the patient. Defaults to None.
            medication_id (int, optional): The medication ID prescribed to the patient. Defaults to None.
        """
        self.__appointment_id = appointment_id
        self.__date = date
        self.__timeframe = timeframe
        self.__doctor_hid = doctor_hid
        self.__patient_hid = patient_hid
        self.__room_number = room_number
        self.__status = status
        self.__diagnosis_id = diagnosis_id
        self.__medication_id = medication_id

    def __str__(self) -> str:
        """
        Returns a string representation of the appointment.
        
        Returns:
            str: A string describing the appointment details.
        """
        return f'{self.__date} at {self.__timeframe} with Dr. {self.__doctor_hid} and {self.__patient_hid} in room {self.__room_number} is {self.__status}'
    
    def change_status(self, status: str) -> str: # Change
        """
        Changes the status of the appointment.
        
        Args:
            status (str): The new status of the appointment.
        
        Returns:
            str: A message indicating the new status of the appointment.
        
        Raises:
            ValueError: If the status is not one of 'Scheduled', 'In Progress', 'Completed', or 'Cancelled'.
        """
        if status not in ['Scheduled', 'In Progress', 'Completed', 'Cancelled', 'Rescheduled', 'Pending', 'Rejected']:
            raise ValueError('The status must be either scheduled, completed, or cancelled')
        self.__status = status
        return f'The appointment status is now {self.__status}'
    
    def autocomplete(self) -> None:
        """
        Automatically changes the status of the appointment to completed if the date and time have passed.
        """
        if self.__date < datetime.now().date():
            if self.__timeframe[1] < datetime.now().time():
                self.__status = 'completed'
    
    def change_datetime(self, date: date, timeframe: tuple) -> str: # Change
        """
        Changes the date and time of the appointment.
        
        Args:
            date (date): The new date of the appointment.
            timeframe (tuple): The new time slot for the appointment (start_time, end_time).
        
        Returns:
            str: A message indicating the new date and time of the appointment.
        """
        self.__date = date
        self.__timeframe = timeframe
        return
    
    def change_room(self, room_number: int) -> str:
        """
        Changes the room number of the appointment.
        
        Args:
            room_number (int): The new room number for the appointment.
        
        Returns:
            str: A message indicating the new room number of the appointment.
        """
        self.__room_number = room_number
        return