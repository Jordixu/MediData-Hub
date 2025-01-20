from patient import Patient
from doctor import Doctor
from appointment import Appointment
from room import Room
from notification import Notification
import datetime as dt

class Hospital:
    def __init__(self, name: str, location: str) -> None:
        """
        Initializes the Hospital object.
        Args:
            name (str): The name of the hospital.
            location (str): The location of the hospital.
        """
        
        self.name = name
        self.location = location 
        self.patients = []
        self.doctors = []
        self.appointments = []
        self.rooms = []
        self.drugs = []
        
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
        except ValueError:
            raise ValueError(custom_message_incorrect_type or f"The value must be of type {value_type.__name__}.")
        
        if lower is not None and value < lower:
            raise ValueError(custom_message_lower or f"Value must be greater than {lower}.")
        if upper is not None and value > upper:
            raise ValueError(custom_message_upper or f"Value must be less than {upper}.")
        
        return value

    def add_patient(self, **kwargs) -> str:
        """
        Adds a new patient to the system after validating the provided attributes.
        
        Parameters:
            personal_id (int): Unique identifier for the patient. Must be a positive integer.
            name (str): The patient's first name.
            surname (str): The patient's last name.
            age (int): Age of the patient. Must be a positive integer within a plausible range.
            weight (float): Weight of the patient in kilograms. Must be a positive float within a plausible range.
            height (float): Height of the patient in centimeters. Must be a positive float within a plausible range.
            assigned_doctor (Doctor): The doctor assigned to the patient.
            status (str): The status of the patient (Inpatient, Outpatient, Emergency).
            
        Raises:
            ValueError: If a patient with the same ID already exists or the validation fails.
            
        Returns:
            str: A confirmation message indicating the newly added patient's name and surname.
        """
        
        kwargs['personal_id'] = self.validate_value(kwargs['personal_id'], int, 0, custom_message_incorrect_type="The ID must be a number, without decimals.", custom_message_lower="The ID must be a positive number.")
        kwargs['age'] = self.validate_value(kwargs['age'], int, 0, 150, custom_message_incorrect_type="The age is a number...", custom_message_lower="The age must be a positive number.", custom_message_upper="I don't think you are that old.")
        kwargs['weight'] = self.validate_value(kwargs['weight'], float, 0, 1000, custom_message_incorrect_type="The weight must be a number...", custom_message_lower="The weight must be a positive number.", custom_message_upper="Did you know that the heaviest person ever recorded was 635 kg?, either you are lying or you are a record breaker.")
        kwargs['height'] = self.validate_value(kwargs['height'], float, 0, 300, custom_message_incorrect_type="The height must be a number...", custom_message_lower="The height must be a positive number.", custom_message_upper="Hello, Mr. giant, how can I help you?")
        
        kwargs['hospital_id'] = self.patients[-1].hospital_id + 1 if self.patients else 1
        
        if any(p.personal_id == kwargs['personal_id'] for p in self.patients):
            raise ValueError("The ID is already in our system, perhaps there is a typo?")
        
        new_patient = Patient(**kwargs)
        self.patients.append(new_patient) 
        return f'Patient {new_patient.name} {new_patient.surname} added.'

    def remove_patient(self, patient_personal_id: str) -> str:
        """
        Removes a patient from the system based on their ID.

        Args:
            patient_id (str): The ID of the patient to remove.

        Raises:
            ValueError: If the patient is not found in the system.

        Returns:
            str: A confirmation message indicating the removed patient's name and surname.
        """
        patient_id = self.validate_value(patient_personal_id, int, custom_message_incorrect_type="The ID must be a number.")
        
        for patient in self.patients:
            if patient.personal_id == patient_personal_id:
                self.patients.remove(patient)
                return f'Patient {patient.name} {patient.surname} with ID {patient.id} removed.'
    
        raise ValueError('Patient not found.')

    def add_doctor(self, **kwargs) -> str:
        """
        Adds a new doctor to the system after validating the provided attributes.
        
        Args:
            id (int): Unique identifier for the doctor. Must be a positive integer.
            name (str): The doctor's first name.
            surname (str): The doctor's last name.
            age (int): Age of the doctor. Must be a positive integer within a plausible
            gender (str): The doctor's gender.
            speciality (str): The doctor's speciality.
            department (str): The department the doctor belongs to.
            socialsecurity (int): The doctor's social security number.
            salary (float): The doctor's salary.

        Raises:
            ValueError: If a doctor with the same ID already exists or the validation fails.

        Returns:
            str: A confirmation message indicating the newly added doctor's name and surname.
        """
        kwargs['doctor_id'] = self.validate_value(kwargs['doctor_id'], int, 0)
        kwargs['doctor_age'] = self.validate_value(kwargs['doctor_age'], int, 0, 150)
        kwargs['doctor_socialsecurity'] = self.validate_value(kwargs['doctor_socialsecurity'], int)
        kwargs['doctor_salary'] = self.validate_value(kwargs['doctor_salary'], float, 0)
        
        if any(p.id == kwargs['doctor_id'] for d in self.doctors):
            raise ValueError('Doctor already exists.')
        
        new_doctor = Doctor(**kwargs)
        self.doctors.append(new_doctor)
        return f'Doctor {new_doctor.name} {new_doctor.surname} added.'

    def remove_doctor(self, doctor_id: str) -> str:
        """
        Removes a doctor from the system based on their ID.

        Args:
            doctor_id (str): The ID of the doctor to remove.

        Raises:
            ValueError: If the doctor is not found in the system.

        Returns:
            str: A confirmation message indicating the removed doctor's name and surname.
        """
        doctor_id = self.validate_value(doctor_id, int, custom_message="The ID must be a number.")

        for doctor in self.doctors:
            if doctor.id == doctor_id:
                self.doctors.remove(doctor)
                return f'Doctor {doctor.name} {doctor.surname} with ID {doctor.id} removed.'

        raise ValueError('Doctor not found.')

    def _check_availability(self, doctor, date, timeframe):
        return doctor.availabilities.get(date, {}).get(timeframe, False)

    def _schedule_appointment(self, patient, doctor, date, timeframe, room):
        new_appointment = Appointment(date, timeframe, doctor, patient, room, status=True)
        self.appointments.append(new_appointment)
        doctor.availabilities[date][timeframe] = False
        room.availability[date][timeframe] = False
        doctor.add_appointment(new_appointment)
        patient.new_appointment(new_appointment)

        # Notifications
        self._send_notification(doctor, f'Appointment scheduled for {date} at {timeframe[0]} for patient {patient.name} {patient.surname}')
        self._send_notification(patient, f'Appointment scheduled for {date} at {timeframe[0]} by Dr. {doctor.name} {doctor.surname}')
        return f'Appointment scheduled for {date}'

    def _send_notification(self, recipient, message):
        notification = Notification(message)
        recipient.add_notification(notification)

    def schedule_appointment(self, patient: Patient, doctor: Doctor, date: str, timeframe: tuple) -> str:
        if doctor not in self.doctors:
            return 'Doctor not found, please introduce the correct ID'
        if not self._check_availability(doctor, date, timeframe):
            return f'Dr. {doctor.surname} is not available at that time, please choose another date or timeframe'

        for room in self.spaces:
            if room.availability.get(date, {}).get(timeframe, False):
                return self._schedule_appointment(patient, doctor, date, timeframe, room)
        return 'No available rooms, please choose another date or timeframe'

    def cancel_appointment(self, patient: Patient, doctor: Doctor, date: str, timeframe: tuple) -> str:
        for appointment in self.appointments:
            if appointment.patient == patient and appointment.doctor == doctor and appointment.date == date and appointment.timeframe == timeframe:
                self.appointments.remove(appointment)
                doctor.availabilities[date][timeframe] = True
                self.spaces[appointment.room].availability[date][timeframe] = True
                doctor.remove_appointment(appointment)
                patient.remove_appointment(appointment)

                self._send_notification(doctor, f'Appointment cancelled for {date} at {timeframe[0]} for patient {patient.name} {patient.surname}')
                self._send_notification(patient, f'Appointment cancelled for {date} at {timeframe[0]} by Dr. {doctor.name} {doctor.surname}')
                return f'Appointment cancelled for {date}'
        return 'Appointment not found'