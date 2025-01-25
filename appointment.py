from datetime import date, time, datetime
from doctor import Doctor
from patient import Patient
from room import Room
class Appointment():
    def __init__(self, appointment_id: int, date: date, timeframe: tuple, doctor: Doctor, patient: Patient, room: Room, status:str, diagnosis:str = None, medication = None, notes:str = None) -> None:
        """
        Initialize an Appointment instance.
        Args:
            date (date): The date of the appointment.
            timeframe (tuple): The time slot for the appointment (start_time, end_time).
            doctor (Doctor): The doctor assigned to the appointment.
            patient (Patient): The patient scheduled for the appointment.
            room (Room): The room assigned for the appointment.
            status (str): The current status of the appointment.
        """

        self.appointment_id = appointment_id
        self.__date = date
        self.__timeframe = timeframe
        self.__doctor = doctor
        self.__patient = patient
        self.__room = room
        self.__status = status
        self.__diagnosis = diagnosis
        self.__medication = medication
        self.__notes = notes

    def __str__(self) -> str:
        return f'{self.__date} at {self.__timeframe} with Dr. {self.__doctor} and {self.__patient} in room {self.__room} is {self.__status}'
    
    def get_date(self) -> date:
        return self.__date
    
    def get_time(self) -> tuple:
        return self.__timeframe
    
    def get_doctor(self) -> Doctor:
        return self.__doctor
    
    def get_patient(self) -> Patient:
        return self.__patient
    
    def get_room(self) -> Room:
        return self.__room
    
    def change_status(self, status: str) -> str:
        if status not in ['Scheduled', 'In Progress', 'Completed', 'Cancelled']:
            raise ValueError('The status must be either scheduled, completed, or cancelled')
        self.__status = status
        return f'The appointment status is now {self.__status}'
    
    def autocomplete(self) -> None:
        if self.__date < datetime.now().date():
            if self.__timeframe[1] < datetime.now().time():
                self.__status = 'completed'
    
    def change_date(self, date: date) -> str:
        self.__date = date
    
    # def change_time(self, timeframe: tuple) -> str:
    #     # Check if the doctor is available
    #     if not self.doctor.availabilities[self.__date][timeframe]:
    #         return f'Dr. {self.doctor} is not available at {timeframe}'
    #     # Check if the room is available
    #     if not self.__room.availabilities[self.__date][timeframe]:
    #         return f'The room {self.__room.__number} is not available at {timeframe}'
        
    #     self.timeframe = timeframe
    #     return f'The appointment is now scheduled at {self.timeframe}'
    
    def change_doctor(self, doctor: Doctor) -> str:
        if doctor == self.__doctor:
            return f'The appointment is already with Dr. {self.__doctor}'
        self.__doctor = doctor
        return f'The appointment is now with Dr. {self.__doctor}'
    
    def change_patient(self, patient: Patient) -> str:
        self.__patient = patient
    
    def change_room(self, room: Room) -> str:
        self.__room = room
        
    def get_all_attributes(self) -> dict:
        return self.__dict__