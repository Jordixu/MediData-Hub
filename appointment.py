from datetime import date, time, datetime
from doctor import Doctor
from patient import Patient
from room import Room
class Appointment():
    def __init__(self, date: date, timeframe: tuple, doctor: Doctor, patient: Patient, room: Room, status:str) -> None:
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

        self.date = date
        self.time = timeframe
        self.doctor = doctor
        self.patient = patient
        self.room = room
        self.status = status

    def __str__(self) -> str:
        return f'{self.date} at {self.timeframe} with Dr. {self.doctor}'
    
    def change_status(self, status: str) -> str:
        if status not in ['scheduled', 'completed', 'cancelled']:
            raise ValueError('The status must be either scheduled, completed, or cancelled')
        self.status = status
        return f'The appointment status is now {self.status}'
    
    def autocomplete(self) -> None:
        if self.date < datetime.now().date():
            if self.timeframe[1] < datetime.now().time():
                self.status = 'completed'
    
    def change_date(self, date: date) -> str:
        self.date = date
    
    def change_time(self, timeframe: tuple) -> str:
        # Check if the doctor is available
        if not self.doctor.availabilities[self.date][timeframe]:
            return f'Dr. {self.doctor} is not available at {timeframe}'
        # Check if the room is available
        if not self.room.availabilities[self.date][timeframe]:
            return f'The room {self.room.number} is not available at {timeframe}'
        
        self.timeframe = timeframe
        return f'The appointment is now scheduled at {self.timeframe}'
    
    def change_doctor(self, doctor: Doctor) -> str:
        if doctor == self.doctor:
            return f'The appointment is already with Dr. {self.doctor}'
        self.doctor = doctor
        return f'The appointment is now with Dr. {self.doctor}'
    
    def change_patient(self, patient: Patient) -> str:
        self.patient = patient
    
    def change_room(self, room: Room) -> str:
        self.room = room