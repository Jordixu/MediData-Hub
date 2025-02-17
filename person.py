from foundation import Foundation
from datetime import date
from typing import Union
class Person(Foundation):
    """
    The base class for all people in the hospital.
    
    Attributes:
        personal_id (int): The personal ID of the person.
        hospital_id (int): The hospital ID of the person.
        password (str): The password for the person's account.
        name (str): The first name of the person.
        surname (str): The surname of the person.
        birthday (date): The birth date of the person
    
    Methods:
        get(attribute): Returns the value of the attribute.
        get_private_info(attribute): Returns the value of a private attribute.
        set_private_info(attribute, value): Changes the value of a private attribute.
        __name__(): Returns the full name of the person.
        check_password(password): Checks if the password is correct.
        set_info(attribute, value, type): Changes the value of an attribute.
        add_notification(notification_id): Adds a notification to the person.
        display_last_notification(): Displays the last notification the person received.
        add_appointment(appointment_id): Adds an appointment to the person.
    """
    def __init__(self, personal_id: int, hospital_id: int, password: str, name: str, surname: str, birthday: date, gender: str, appointments: list = None, notifications: list = None):
        self._personal_id = personal_id
        self._hospital_id = hospital_id
        self._password = password
        self._name = name
        self._surname = surname
        self._birthday = birthday
        self._gender = gender
        self._appointments = appointments if appointments is not None else []
        self._notifications = notifications if notifications is not None else []
        
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