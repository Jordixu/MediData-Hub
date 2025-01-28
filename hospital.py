import datetime as dt

from patient import Patient
from doctor import Doctor
from appointment import Appointment
from room import Room
from notification import Notification

class Hospital:
    """
    Represents a hospital with patients, doctors, appointments, and rooms.
    
    Attributes:
        name (str): The name of the hospital.
        location (str): The location of the hospital.
        patients (list): A list of patients in the hospital.
        doctors (list): A list of doctors in the hospital.
        appointments (list): A list of appointments in the hospital.
        rooms (list): A list of rooms in the hospital.
        drugs (list): A list of drugs in the hospital.
        notifications (list): A list of notifications in the hospital.
        
    Methods:
        checkadmin(username, password): Checks if the username and password match the admin credentials.
        load_data(): Loads data from CSV files into the hospital system.
        validate_value(value, value_type, lower, upper, custom_message_incorrect_type, custom_message_lower, custom_message_upper): Validates the given value by casting it to a specified type and optionally checking if it falls within lower and upper bounds.
        add_patient(**kwargs): Adds a new patient to the system after validating the provided attributes.
        remove_patient(patient_id): Removes a patient from the system based on their ID.
        add_doctor(**kwargs): Adds a new doctor to the system after validating the provided attributes.
        remove_doctor(doctor_id): Removes a doctor from the system based on their ID.
        schedule_appointment(patient_hid, doctor_hid, date, timeframe): Schedules an appointment between a patient and a doctor.
        cancel_appointment(patient_hid, doctor_hid, date, timeframe): Cancels an appointment between a patient and a doctor.
        send_notification(receiver, sender, message): Sends a notification from the sender to the receiver with the given message.
        search_appointments(search_term): Searches for appointments based on the given search term.
        get_appointment(appointment_id): Retrieves an appointment based on the given appointment ID.
        delete_appointment(appointment_id): Deletes an appointment based on the given appointment ID.
        get_appointments(): Retrieves all appointments in the system.
    """
    def __init__(self, username: str, password: str, utility) -> None:
        """
        Initializes the Hospital object.
        Args:
            name (str): The name of the hospital.
            location (str): The location of the hospital.
        """
        self.__admin_username = username
        self.__admin_password = password
        self.patients = []
        self.doctors = []
        self.appointments = []
        self.rooms = []
        self.drugs = []
        self.notifications = []
        self.utility = utility

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
        This method attempts to load data for patients, doctors, appointments, and rooms
        from their respective CSV files located in the './database/' directory. It handles
        missing files and type errors by printing appropriate messages.
        Raises:
            FileNotFoundError: If any of the required files are not found.
        Notes:
            - Patient data is loaded from 'patients.csv' and transformed to match the Patient class.
            - Doctor data is loaded from 'doctors.csv' and transformed to match the Doctor class.
            - Appointment data is loaded from 'appointments.csv' and transformed to match 
            Appointment class.
            - Room data is loaded from 'rooms.csv' and transformed to match the Room class.
        """

        try:
            patients = self.utility.load_from_csv('./database/patients.csv')
            for patient in patients:
                new_patient = Patient(**patient)
                self.patients.append(new_patient)
                print(new_patient)
        except FileNotFoundError as exc:
            raise FileNotFoundError("No patients found in the database") from exc
        except TypeError as e:
            print(f"Incorrect type: {e}")

        try:
            doctors = self.utility.load_from_csv('./database/doctors.csv')
            for doctor in doctors:
                new_doctor = Doctor(**doctor)
                self.doctors.append(new_doctor)
        except FileNotFoundError as exc:
            raise FileNotFoundError("No doctors found in the database") from exc

        except TypeError as e:
            print(f"Incorrect type: {e}")

        try:
            for appointment in self.utility.load_from_csv('./database/appointments.csv'):
                new_appointment = Appointment(**appointment)
                self.appointments.append(new_appointment)
        except FileNotFoundError as exc:
            raise FileNotFoundError("No appointments found in the database") from exc
        except TypeError as e:
            print(f"Incorrect type: {e}")

        try:
            for room in self.utility.load_from_csv('./database/rooms.csv'):
                self.rooms.append(Room(**room))
        except FileNotFoundError as exc:
            raise FileNotFoundError('No rooms found in the database') from exc
        except TypeError as e:
            print(f"Incorrect type: {e}")

        # try:
        #     for drug in self.utility.load_from_csv('./database/drugs.csv'):
        #         self.drugs.append(Drug(**drug))
        # except FileNotFoundError:
        #     raise FileNotFoundError('No drugs found in the database')

    #@staticmethod
    def validate_value(self, value: any,value_type: object, lower: int|float = None, upper: int|float = None, custom_message_incorrect_type: str = None, custom_message_lower: str = None, custom_message_upper: str = None) -> object: # quizás integremos esto fuera de la clase Hospital o lo definimos como staticmethod para usarlo fuera
        """
        Validates the given value by casting it to a specified type and optionally checking if it falls within lower and upper bounds.
        
        Args:
            value (Any): The value to validate.
            value_type (type): The expected type to cast the value to.
            lower (int | float, optional): The lower bound for the value. Defaults to None.
            upper (int | float, optional): The upper bound for the value. Defaults to None.
            custom_message_incorrect_type (str, optional): A custom error message if the value is not of the expected type. Defaults to None.
            custom_message_lower (str, optional): A custom error message if the value is lower than the lower bound. Defaults to None.
            custom_message_upper (str, optional): A custom error message if the value is greater than the upper bound. Defaults to None.
            
        Raises:
            ValueError: If casting fails or the value falls outside the specified bounds.
            
        Returns:
            Any: The validated (and possibly cast) value.
        """
        try:
            value = value_type(value)
        except ValueError as exc:
            raise ValueError(custom_message_incorrect_type or f"The value must be of type {value_type.__name__}.") from exc
        
        if lower is not None and value < lower:
            raise ValueError(custom_message_lower or f"Value must be greater than {lower}.")
        if upper is not None and value > upper:
            raise ValueError(custom_message_upper or f"Value must be less than {upper}.")

        return value

    def add_patient(self, **kwargs) -> bool:
        """
        Adds a new patient to the system after validating the provided attributes.
        
        Parameters:
            personal_id (int): Unique identifier for the patient. Must be a positive integer.
            name (str): The patient's first name.
            surname (str): The patient's last name.
            birthday (date): Birthday of the patient. Must be a date within a plausible range.
            weight (float): Weight of the patient in kilograms. Must be a positive float within a plausible range.
            height (float): Height of the patient in centimeters. Must be a positive float within a plausible range.
            assigned_doctor (Doctor): The doctor assigned to the patient.
            status (str): The status of the patient (Inpatient, Outpatient, Emergency).
            
        Raises:
            ValueError: If a patient with the same ID already exists or the validation fails.
            
        Returns:
            bool: True if the patient was successfully added
        """

        kwargs['personal_id'] = self.validate_value(kwargs['personal_id'], int, 0, custom_message_incorrect_type="The ID must be a number, without decimals.", custom_message_lower="The ID must be a positive number.")
        kwargs['weight'] = self.validate_value(kwargs['weight'], float, 0, 1000, custom_message_incorrect_type="The weight must be a number...", custom_message_lower="The weight must be a positive number.", custom_message_upper="Did you know that the heaviest person ever recorded was 635 kg?, either you are lying or you are a record breaker.")
        kwargs['height'] = self.validate_value(kwargs['height'], float, 0, 300, custom_message_incorrect_type="The height must be a number...", custom_message_lower="The height must be a positive number.", custom_message_upper="Hello, Mr. giant, how can I help you?")

        if not (dt.date(1900, 1, 1) <= kwargs['birthday'] <= dt.date.today()):
            raise ValueError("The birthday must be between 1900-01-01 and today.")

        if any(p.get_protected_attribute('personal_id') == kwargs['personal_id'] for p in self.patients):
            raise ValueError("The ID is already in our system, perhaps there is a typo?")

        if 'hospital_id' not in kwargs:
            kwargs['hospital_id'] = self.patients[-1].get_protected_attribute("hospital_id") + 1 if self.patients else 1

        new_patient = Patient(**kwargs)
        self.patients.append(new_patient)
        if new_patient not in self.patients:
            raise ValueError("The patient could not be added.")
        return True

    def remove_patient(self, patient_hospital_id: int|str) -> str:
        """
        Removes a patient from the system based on their ID.

        Args:
            patient_id (int|str): The ID of the patient to remove.

        Raises:
            ValueError: If the patient is not found in the system.
        """
        patient_hospital_id = self.validate_value(patient_hospital_id, int, custom_message_incorrect_type="The ID must be a number.")
        
        for patient in self.patients:
            if patient.get_protected_attributes("hospital_id") == int(patient_hospital_id):
                self.patients.remove(patient)
                return
    
        raise ValueError('Patient not found.')

    def add_doctor(self, **kwargs) -> None:
        """
        Adds a new doctor to the system after validating the provided attributes.
        
        Args:
            personal_id (int): Unique identifier for the doctor. Must be a positive integer.
            hospital_id (int): Unique hospital identifier for the doctor. Generated automatically.
            name (str): The doctor's first name.
            surname (str): The doctor's last name.
            birthday (int): Birthday of the doctor. Must be a date within a plausible range.
            gender (str): The doctor's gender.
            speciality (str): The doctor's speciality.
            department (str): The department the doctor belongs to.
            socialsecurity (int): The doctor's social security number.
            salary (float): The doctor's salary.

        Raises:
            ValueError: If a doctor with the same ID already exists or the validation fails.
        """
        kwargs['personal_id'] = self.validate_value(kwargs['personal_id'], int, 0)
        kwargs['hospital_id'] = self.validate_value(kwargs['hospital_id'], int, 0)
        kwargs['birthday'] = self.validate_value(kwargs['birthday'], dt.date, 0, 150)
        kwargs['socialsecurity'] = self.validate_value(kwargs['socialsecurity'], int)
        kwargs['salary'] = self.validate_value(kwargs['salary'], float, 0)
        
        if any(d.get_protected_info("personal_id") == kwargs['personal_id'] for d in self.doctors):
            raise ValueError('Doctor already exists.')
        
        # Hospital_id for doctors will start at 1000
        if 'hospital_id' not in kwargs:
            kwargs['hospital_id'] = self.doctors[-1].hospital_id + 1 if self.doctors else 1000
        
        new_doctor = Doctor(**kwargs)
        self.doctors.append(new_doctor)

    def remove_doctor(self, doctor_id: int|str) -> None:
        """
        Removes a doctor from the system based on their ID.

        Args:
            doctor_id (str): The ID of the doctor to remove.

        Raises:
            ValueError: If the doctor is not found in the system.
        """
        doctor_id = self.validate_value(doctor_id, int, custom_message_incorrect_type="The ID must be a number.")

        for doctor in self.doctors:
            if doctor.get_protected_info("hospital_id") == doctor_id:
                self.doctors.remove(doctor)
                return

        raise ValueError('Doctor not found.')

    def schedule_appointment(self, patient_hid: int, doctor_hid: int, date: dt.date, timeframe: tuple) -> str:
        """
        Schedules an appointment between a patient and a doctor.
        
        Args:
            patient_hid (int): The hospital ID of the patient.
            doctor_hid (int): The hospital ID of the doctor.
            date (str): The date of the appointment.
            timeframe (tuple): The timeframe of the appointment.
        
        Returns:
            str: A confirmation message or an error message.
        """
        
        # Find the doctor
        doctor = next((doc for doc in self.doctors if doc.get_protected_info("hospital_id") == doctor_hid), None)
        if not doctor:
            raise ValueError('Doctor not found')
        
        # Find the patient
        patient = next((pat for pat in self.patients if pat.get_protected_info("hospital_id") == patient_hid), None)
        if not patient:
            raise ValueError('Patient not found')
        
        # Check if the doctor is available
        if not doctor.check_availability(date, timeframe):
            return f'Dr. {doctor.surname} is not available at that time, please choose another date or timeframe'

        for room in self.rooms:
            if room.check_availability(date, timeframe):
                doctor.change_availability(date, timeframe)
                room.change_availability(date, timeframe)
                appointment_id = self.appointments[-1].id + 1 if self.appointments else 1
                appointment = Appointment(appointment_id, date, timeframe, doctor_hid, patient_hid, room.get("number"), 'scheduled')
                self.appointments.append(appointment)
                doctor.add_appointment(appointment.get('appointment_id'))
                patient.add_appointment(appointment.get('appointment_id'))
                return f'Appointment scheduled with Dr. {doctor.surname} on {date} at {timeframe}'
        
        return 'No available rooms, please choose another date or timeframe'

    # def cancel_appointment(self, patient: Patient, doctor: Doctor, date: str, timeframe: tuple) -> str:
    #     for appointment in self.appointments:
    #         if appointment.patient == patient and appointment.doctor == doctor and appointment.date == date and appointment.timeframe == timeframe:
    #             doctor.availabilities[date][timeframe] = True
    #             self.rooms[appointment.room].availability[date][timeframe] = True
    #             appointment.change_status('cancelled')

    #             self.send_notification(patient, doctor, f'Your appointment on {date} has been cancelled.')
    #             self.send_notification(doctor, patient, f'Your appointment on {date} has been cancelled.')
    #             return f'Appointment cancelled for {date}'
    #     return 'Appointment not found'
    
    def send_notification(self, receiver_hid, sender_hid, message):
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
        self.notifications.append(Notification(message, date, sender_hid, receiver_hid)) # FALTA IMPLEMENTAR EL METODO PARA QUE LOS DOCTORES Y PACIENTES PUEDAN VER SUS NOTIFICACIONES
        
    def search_appointments(self, search_term: str) -> list: # Hay que cambiar esto para que busque en todos los atributos de Appointment
        """
        Searches for appointments based on the given search term.
        Args:
            search_term (str): The term to search for in the appointments.
        Returns:
            list: A list of appointments that match the search term.
        """
        return [appointment for appointment in self.appointments if search_term in str(appointment)] # MODIFY
    
    def get_appointment(self, appointment_id: int) -> Appointment:
        """
        Retrieves an appointment based on the given appointment ID.
        Args:
            appointment_id (int): The ID of the appointment to retrieve.
        Returns:
            Appointment: The appointment object that matches the given ID.
        """
        for appointment in self.appointments:
            if appointment.id == appointment_id: # MODIFY
                return appointment
        return None
    
    def delete_appointment(self, appointment_id: int) -> None:
        """
        Deletes an appointment based on the given appointment ID.
        Args:
            appointment_id (int): The ID of the appointment to delete.
        """
        for appointment in self.appointments:
            if appointment.id == appointment_id: # MODIFY
                self.appointments.remove(appointment)
                return
        return None
    
    def get_appointments(self) -> list: # mmm no se si es buena idea devolver la lista de appointments directamente, quizas deberiamas devolver los ids y ya
        """
        Retrieves all appointments in the system.
        Returns:
            list: A list of all appointments in the system.
        """
        return self.appointments
