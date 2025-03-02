import datetime as dt
from foundation import Foundation
import numpy as np

class Appointment(Foundation):
    def __init__(self, appointment_id: int, date: dt.date, timeframe: tuple, doctor_hid: int, patient_hid: int, status: str, room_number: int = None, diagnosis_id: int = None, medication_id: int = None) -> None:
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
        if self.__date < dt.datetime.now().date():
            if self.__timeframe[1] < dt.datetime.now().time():
                self.__status = 'completed'
    
    def change_datetime(self, date: dt.date, timeframe: tuple) -> str: # Change
        """
        Changes the date and time of the appointment.
        
        Args:
            date (date): The new date of the appointment.
            timeframe (tuple): The new time slot for the appointment (start_time, end_time).
        
        Returns:
            str: A message indicating the new date and time of the appointment.
        """
        if not isinstance(date, dt.date) or not isinstance(timeframe, tuple):
            raise ValueError('The date and timeframe must be of type date and tuple')
        
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
        self.__room_number = int(room_number)
        return