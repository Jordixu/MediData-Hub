from datetime import date, time, datetime
from doctor import Doctor
from patient import Patient
from room import Room
from foundation import Foundation
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
        diagnosis (str): The diagnosis of the patient.
        medication (str): The medication prescribed to the patient.
        
    Methods:
        change_status(status): Changes the status of the appointment.
        autocomplete(): Automatically changes the status of the appointment to completed if the date and time have passed.
        change_datetime(date, timeframe): Changes the date and time of the appointment.
        change_time(timeframe): Changes the time of the appointment.
        change_doctor(doctor_hid): Changes the doctor assigned to the appointment.
    """
    def __init__(self, appointment_id: int, date: date, timeframe: tuple, doctor_hid: int, patient_hid: int, room_number: int, status:str, diagnosis_id:str = None, medication_id = None) -> None:
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
            diagnosis (str, optional): The diagnosis of the patient. Defaults to None.
            medication (str, optional): The medication prescribed to the patient. Defaults to None.
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
        return f'{self.__date} at {self.__timeframe} with Dr. {self.__doctor_hid} and {self.__patient_hid} in room {self.__room_number} is {self.__status}'
    
    def change_status(self, status: str) -> str:
        if status not in ['Scheduled', 'In Progress', 'Completed', 'Cancelled']:
            raise ValueError('The status must be either scheduled, completed, or cancelled')
        self.__status = status
        return f'The appointment status is now {self.__status}'
    
    def autocomplete(self) -> None:
        if self.__date < datetime.now().date():
            if self.__timeframe[1] < datetime.now().time():
                self.__status = 'completed'
    
    def change_datetime(self, date: date, timeframe: tuple) -> str: # Check if everything is available
        self.__date = date
        self.__timeframe = timeframe
        return f'The appointment is now scheduled on {self.__date} at {self.__timeframe}'
    
    # def change_time(self, timeframe: tuple) -> str:
    #     # Check if the doctor is available
    #     if not self.doctor.availabilities[self.__date][timeframe]:
    #         return f'Dr. {self.doctor} is not available at {timeframe}'
    #     # Check if the room is available
    #     if not self.__room.availabilities[self.__date][timeframe]:
    #         return f'The room {self.__room.__number} is not available at {timeframe}'
        
    #     self.timeframe = timeframe
    #     return f'The appointment is now scheduled at {self.timeframe}'
    
    def change_doctor(self, doctor_hid: Doctor) -> str:
        if doctor_hid == self.__doctor_hid:
            return f'The appointment is already with Dr. {self.__doctor_hid}'
        self.__doctor_hid = doctor_hid
        return f'The appointment is now with Dr. {self.__doctor_hid}'