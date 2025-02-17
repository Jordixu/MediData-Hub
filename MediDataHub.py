import datetime as dt
from typing import Union
from patient import Patient
from doctor import Doctor
from appointment import Appointment
from room import Room
from notification import Notification
from utilities import Utilities

class Hospital:
    """
    Represents a hospital system.
    
    Attributes:
        name (str): The name of the hospital.
        location (str): The location of the hospital.
        patients (dict): A dictionary of patients in the hospital.
        doctors (dict): A dictionary of doctors in the hospital.
        appointments (dict): A dictionary of appointments in the hospital.
        rooms (dict): A dictionary of rooms in the hospital.
        drugs (dict): A dictionary of drugs in the hospital.
        notifications (dict): A dictionary of notifications in the hospital.
        
    Methods:
        change_admin_credentials(username, password): Changes the admin credentials.
        checkadmin(username, password): Checks if the username and password match the admin credentials.
        load_data(): Loads data from CSV files into the hospital system.
        add_patient(**kwargs): Adds a new patient to the system after validating the provided attributes.
        remove_patient(patient_id): Removes a patient from the system based on their ID.
        add_doctor(**kwargs): Adds a new doctor to the system after validating the provided attributes.
        remove_doctor(doctor_id): Removes a doctor from the system based on their ID.
        schedule_appointment(patient_id, doctor_id, date, timeframe): Schedules an appointment between a patient and a doctor.
        cancel_appointment(appointment_id): Cancels an appointment between a patient and a doctor.
        send_notification(receiver_id, sender_id, message): Sends a notification from the sender to the receiver with the given message.
        search_appointments(search_term): Searches for appointments based on the given search term.
        get_appointment(appointment_id): Retrieves an appointment based on the given appointment ID.
        get_appointments(): Retrieves all appointments in the system.
    """
    def __init__(self, username: str, password: str, utility: Utilities) -> None:
        """
        Initializes the Hospital object.
        
        Args:
            username (str): The admin username.
            password (str): The admin password.
            utility: Utility object for various operations.
        """
        self.__admin_username = username
        self.__admin_password = password
        self.patients = {}
        self.doctors = {}
        self.appointments = {}
        self.rooms = {}
        self.drugs = {}
        self.notifications = {}
        self.utility = utility
        
    def change_admin_credentials(self, username: str, password: str) -> None:
        """
        Changes the admin credentials.
        
        Args:
            username (str): The new username for the admin.
            password (str): The new password for the admin.
        """
        self.__admin_username = username
        self.__admin_password = password

    def checkadmin(self, username: str, password: str) -> bool:
        """
        Checks if the username and password match the admin credentials.
        
        Args:
            username (str): The username to check.
            password (str): The password to check.
        
        Returns:
            bool: True if the credentials match, False otherwise.
        """
        return username == self.__admin_username and password == self.__admin_password

    def load_data(self):
        """
        Loads data from CSV files into the hospital system.
        
        This method creates the instances of the required class and appends it into the hospital system to be used. It handles the errors in case the files are not found.
        
        Raises:
            FileNotFoundError: If any of the required files are not found.
            TypeError: If the data in the files is not of the expected type.
        """
        try:
            patients = self.utility.load_from_csv('./database/patients.csv')
            for patient in patients:
                new_patient = Patient(**patient)
                self.patients[new_patient.get_protected_attribute('hospital_id')] = new_patient
        except FileNotFoundError as exc:
            raise FileNotFoundError("No patients found in the database") from exc
        except TypeError as e:
            print(f"Incorrect type: {e}")

        try:
            doctors = self.utility.load_from_csv('./database/doctors.csv')
            for doctor in doctors:
                # print("Notifications before:", doctor['notifications'])
                new_doctor = Doctor(**doctor)
                # print("Notifications:", new_doctor.get_protected_attribute('notifications'))
                self.doctors[new_doctor.get_protected_attribute('hospital_id')] = new_doctor
        except FileNotFoundError as exc:
            raise FileNotFoundError("No doctors found in the database") from exc
        except TypeError as e:
            print(f"Incorrect type: {e}")

        try:
            for appointment in self.utility.load_from_csv('./database/appointments.csv'):
                new_appointment = Appointment(**appointment)
                self.appointments[new_appointment.get('appointment_id')] = new_appointment
        except FileNotFoundError as exc:
            raise FileNotFoundError("No appointments found in the database") from exc
        except TypeError as e:
            print(f"Incorrect type: {e}")

        try:
            for room in self.utility.load_from_csv('./database/rooms.csv'):
                new_room = Room(**room)
                self.rooms[new_room.get('number')] = new_room
        except FileNotFoundError as exc:
            raise FileNotFoundError('No rooms found in the database') from exc
        except TypeError as e:
            print(f"Incorrect type: {e}")
            
        try:
            for notification in self.utility.load_from_csv('./database/notifications.csv'):
                new_notification = Notification(**notification)
                self.notifications[new_notification.get('notification_id')] = new_notification
                # print("Notification:", new_notification)
        except FileNotFoundError as exc:
            raise FileNotFoundError('No notifications found in the database') from exc
        except TypeError as e:
            print(f"Incorrect type: {e}")

    def add_patient(self, **kwargs) -> bool:
        """
        Adds a new patient to the system after validating the provided attributes.
        
        Args:
            **kwargs: Dictionary of the attributes of the patient to be added.
        
        Raises:
            ValueError: If a patient with the same ID already exists or the validation fails.
        
        Returns:
            bool: True if the patient was successfully added.
        """
        kwargs['personal_id'] = self.utility.validate_and_cast_value(kwargs['personal_id'], int, 0, custom_message_incorrect_type="The ID must be a number, without decimals.", custom_message_lower="The ID must be a positive number.")
        kwargs['weight'] = self.utility.validate_and_cast_value(kwargs['weight'], float, 0, 1000, custom_message_incorrect_type="The weight must be a number...", custom_message_lower="The weight must be a positive number.", custom_message_upper="Did you know that the heaviest person ever recorded was 635 kg?, either you are lying or you are a record breaker.")
        kwargs['height'] = self.utility.validate_and_cast_value(kwargs['height'], float, 0, 300, custom_message_incorrect_type="The height must be a number...", custom_message_lower="The height must be a positive number.", custom_message_upper="Hello, Mr. giant, how can I help you?")

        if not (dt.date(1900, 1, 1) <= kwargs['birthday'] <= dt.date.today()):
            raise ValueError("The birthday must be between 1900-01-01 and today.")

        if any(p.get_protected_attribute('personal_id') == kwargs['personal_id'] for p in self.patients.values()):
            raise ValueError("The ID is already in our system, perhaps there is a typo?")

        if 'hospital_id' not in kwargs:
            kwargs['hospital_id'] = max(self.patients.keys(), default=0) + 1

        new_patient = Patient(**kwargs)
        self.patients[new_patient.get_protected_attribute('hospital_id')] = new_patient
        return True

    def remove_patient(self, patient_hospital_id: Union[int, str]) -> str:
        """
        Removes a patient from the system based on their ID.
        
        Args:
            patient_hospital_id (Union[int, str]): The ID of the patient to remove.
        
        Raises:
            ValueError: If the patient is not found in the system.
        """
        patient_hospital_id = self.utility.validate_and_cast_value(patient_hospital_id, int, custom_message_incorrect_type="The ID must be a number.")
        
        if patient_hospital_id in self.patients:
            del self.patients[patient_hospital_id]
            return
    
        raise ValueError('Patient not found.')

    def add_doctor(self, **kwargs) -> None:
        """
        Adds a new doctor to the system after validating the provided attributes.
        
        Args:
            **kwargs: Dictionary of the attributes of the doctor to be added.
        
        Raises:
            ValueError: If a doctor with the same ID already exists or the validation fails.
        """
        kwargs['personal_id'] = self.utility.validate_and_cast_value(kwargs['personal_id'], int, 0)
        kwargs['hospital_id'] = self.utility.validate_and_cast_value(kwargs['hospital_id'], int, 0)
        kwargs['birthday'] = self.utility.validate_and_cast_value(kwargs['birthday'], dt.date, 0, 150)
        kwargs['socialsecurity'] = self.utility.validate_and_cast_value(kwargs['socialsecurity'], int)
        kwargs['salary'] = self.utility.validate_and_cast_value(kwargs['salary'], float, 0)
        
        if any(d.get_protected_info("personal_id") == kwargs['personal_id'] for d in self.doctors.values()):
            raise ValueError('Doctor already exists.')
        
        if 'hospital_id' not in kwargs:
            kwargs['hospital_id'] = max(self.doctors.keys(), default=999) + 1
        
        new_doctor = Doctor(**kwargs)
        self.doctors[new_doctor.get_protected_attribute('hospital_id')] = new_doctor

    def remove_doctor(self, doctor_id: Union[int, str]) -> None:
        """
        Removes a doctor from the system based on their ID.
        
        Args:
            doctor_id (Union[int, str]): The ID of the doctor to remove.
        
        Raises:
            ValueError: If the doctor is not found in the system.
        """
        doctor_id = self.utility.validate_and_cast_value(doctor_id, int, custom_message_incorrect_type="The ID must be a number.")

        if doctor_id in self.doctors:
            del self.doctors[doctor_id]
            return

        raise ValueError('Doctor not found.')

    def schedule_appointment(self, patient_hid: int, doctor_hid: int, date: dt.date, timeframe: tuple) -> None:
        """
        Schedules an appointment between a patient and a doctor.
        
        Args:
            patient_hid (int): The hospital ID of the patient.
            doctor_hid (int): The hospital ID of the doctor.
            date (dt.date): The date of the appointment.
            timeframe (tuple): The timeframe of the appointment.
        """
        doctor = self.doctors[doctor_hid]
        if not doctor:
            raise ValueError('Doctor not found')
        
        patient = self.patients[patient_hid]
        if not patient:
            raise ValueError('Patient not found')
        
        if not doctor.check_availability(date, timeframe):
            # print(doctor.get('availability'))
            # print(date, timeframe)
            # print(type(doctor.get('availability')[date]))
            # print(type(doctor.get('availability')[date][timeframe]))
            # print(type(date))
            raise ValueError('Doctor not available at that time')

        try:
            for room in self.rooms.values():
                if room.check_availability(date, timeframe):
                    doctor.change_availability(date, timeframe)
                    room.change_availability(date, timeframe)
                    appointment_id = max(self.appointments.keys(), default=0) + 1
                    appointment = Appointment(appointment_id, date, timeframe, doctor_hid, patient_hid, room.get("number"), 'Scheduled')
                    # print(appointment)
                    self.appointments[appointment_id] = appointment
                    doctor.add_appointment(appointment_id)
                    patient.add_appointment(appointment_id)
                    self.send_notification(patient_hid, doctor_hid, 'Appointment Scheduled', 'Appointment', f'Your appointment with Dr. {doctor.get_protected_attribute("surname")} has been scheduled for {str(date)} at {str(timeframe[0])}')
                    return
                else:
                    continue
            raise ValueError('No available rooms for the appointment')
        except Exception as exc:
            print(exc)
            

    def cancel_appointment(self, appointment_id: int) -> str:
        """
        Cancels an appointment between a patient and a doctor.
        
        Args:
            appointment_id (int): The ID of the appointment to cancel.
        
        Returns:
            str: A confirmation message or an error message.
        """
        appointment = self.appointments.get(appointment_id)
        if not appointment:
            raise ValueError(f"Appointment with ID {appointment_id} not found.")
        
        doctor = self.doctors.get(appointment.get("doctor_hid"))
        if not doctor:
            raise ValueError(f"Doctor associated with appointment ID {appointment_id} not found.")
        
        patient = self.patients.get(appointment.get("patient_hid"))
        if not patient:
            raise ValueError(f"Patient associated with appointment ID {appointment_id} not found.")
        
        appointment.change_status('Cancelled')
        
        self.send_notification(doctor.get_protected_attribute('hospital_id'), patient.get_protected_attribute('hospital_id'), 'Appointment Cancelled', 'Cancellation', f'Your appointment with {patient.get_protected_attribute("name")} {patient.get_protected_attribute("surname")} has been cancelled.')
        
        return

    def send_notification(self, receiver_hid: int, sender_hid: int, title:str, type: str, message: str):
        """
        Sends a notification from the sender to the receiver with the given message.
        
        Args:
            receiver_hid (int): The recipient of the notification.
            sender_hid (int): The sender of the notification.
            message (str): The content of the notification message.
        
        Returns:
            None
        """
        date = dt.datetime.now()
        notification_id = max(self.notifications.keys(), default=0) + 1
        new_notif = Notification(notification_id, title, date, sender_hid, receiver_hid, type, message)
        self.notifications[notification_id] = new_notif
        
        if receiver_hid in self.patients:
            self.patients[receiver_hid].add_notification(notification_id)
        elif receiver_hid in self.doctors:
            self.doctors[receiver_hid].add_notification(notification_id)
        else:
            raise ValueError('Receiver not found')
        

    def search_appointments(self, search_term: str) -> list: # Unfinished
        """
        Searches for appointments based on the given search term.
        
        Args:
            search_term (str): The term to search for in the appointments.
        
        Returns:
            list: A list of appointments that match the search term.
        """
        return [appointment for appointment in self.appointments.values() if search_term in str(appointment)]