from foundation import Foundation
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
    def __init__(self, personal_id, hospital_id, password, name, surname, birthday, gender, appointments = None, notifications = None):
        self._personal_id = personal_id
        self._hospital_id = hospital_id
        self._password = password
        self._name = name
        self._surname = surname
        self._birthday = birthday
        self._gender = gender
        self._appointments = appointments if appointments is not None else {}
        self._notifications = notifications if notifications is not None else []
        
    def __name__(self):
        return self._name + ' ' + self._surname
    
    def check_password(self, password):
        return self._password == password

    def add_notification(self, notification_id):
        self._notifications.append(notification_id)

    def display_last_notification(self):
        return self._notifications[-1]
    
    def add_appointment(self, appointment_id):
        self._appointments.append(appointment_id)