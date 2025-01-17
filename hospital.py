from patient import Patient
from doctor import Doctor
from appointment import Appointment
from space import Space
from notification import Notification
import datetime as dt

class Hospital():
    """
    Represents a hospital with its patients, doctors, appointments and spaces. The functions may be implemented in Administrator class.
    """
    
    def __init__(self, name, location):
        self.name = name # Name of the hospital
        self.location = location # Location of the hospital
        self.patients = [] # List of patients
        self.doctors = [] # List of doctors
        self.appointments = [] # List of appointments
        self.spaces = [] # List of spaces
        
    def add_patient(self, patient_id, patient_name, patient_surname, patient_age, patient_sex, patient_weight, patient_height, patient_assigned_doctor, patient_status):
        """
        Adds a new patient to the hospital system.
        Args:
            patient_id (int or str): ID for the patient.
            patient_name (str): Name of the patient.
            patient_surname (str): Surname of the patient.
            patient_age (int): Age of the patient.
            patient_sex (str): Sex of the patient.
            patient_weight (float): Weight of the patient (in kilograms).
            patient_height (float): Height of the patient (in centimeters).
            patient_assigned_doctor (str): Name of the (family) doctor assigned to the patient.
            patient_status (str): Current status of the patient (e.g., 'admitted', 'discharged'). *AÚN POR DETERMINAR*
        Returns:
            str: A confirmation message stating the patient's addition.
        Raises:
            ValueError: If 'patient_id' is not convertible to an integer or if
                        a patient with the same 'patient_id' already exists.
        """
        try:
            patient_id = int(patient_id) # Check if the ID is a number
        except ValueError: # If not, raise an error
            raise ValueError("The ID must be a number") 

        for patient in self.patients: # Check if the patient already exists
            if patient.id == patient_id:
                raise ValueError('Patient already exists') # If so, raise an error

        new_patient = Patient(patient_id, patient_name, patient_surname, patient_age, patient_sex, patient_weight, patient_height, patient_assigned_doctor, patient_status) # Create a new patient
        self.patients.append(new_patient) # Add the new patient to the list of patients
        return f'Patient {new_patient.name} {new_patient.surname} added' # Return a message confirming the addition of the new patient

            
    def remove_patient(self, patient_id): 
        """
        Removes a patient from the hospital's records by their unique identifier.
        Args:
            patient_id (int or str): The ID for the patient to be removed.
        Returns:
            str: A message indicating the removal success.
        Raises:
            ValueError: If the patient_id is not an integer or 
                        does not exists.
        """
        try:
            patient_id = int(patient_id) # Check if the ID is a number
        except ValueError: # If not, raise an error
            raise ValueError("The ID must be a number")

        for patient in self.patients: # Check if the patient exists
            if patient.id == patient_id:
                self.patients.remove(patient) # If so, remove the patient
                return f'Patient {patient.name} {patient.surname} with ID {patient.id} removed'
    
        raise ValueError('Patient not found') # If the patient does not exist

    def add_doctor(self, doctor_id, doctor_name, doctor_surname, doctor_age, doctor_sex, doctor_speciality, doctor_department, doctor_socialsecurity, doctor_salary):
        """
        Adds a new doctor to the hospital's list of doctors.
        Args:
            doctor_id (int or str): Unique identifier for the doctor.
            doctor_name (str): First name of the doctor.
            doctor_surname (str): Surname of the doctor.
            doctor_age (int): Age of the doctor.
            doctor_sex (str): Gender of the doctor.
            doctor_speciality (str): Specialist field of the doctor.
            doctor_department (str): Department where the doctor works.
            doctor_socialsecurity (str): Social security information of the doctor.
            doctor_salary (float): Salary of the doctor.
        Returns:
            str: A message confirming that the doctor has been added.
        Raises:
            ValueError: If the doctor_id is not a valid number or 
                        if the doctor already exists.
        """
        try:
            doctor_id = int(doctor_id)
        except ValueError:
            raise ValueError('The ID must be a number')
        
        for doctor in self.doctors:
            if doctor.id == doctor_id:
                raise ValueError('Doctor already exists')
        
        new_doctor = Doctor(doctor_id, doctor_name, doctor_surname, doctor_age, doctor_sex, doctor_speciality, doctor_department, doctor_socialsecurity, doctor_salary)
        self.doctors.append(new_doctor)
        return f'Doctor {new_doctor.name} {new_doctor.surname} added'

    def remove_doctor(self, doctor_id):
        """
        Removes a doctor from the list by the provided ID.
        Args:
            doctor_id (int or str): The numeric identifier of the doctor
                to be removed. If given as a string, an attempt will be
                made to convert it to an integer.
        Returns:
            str: A confirmation message indicating that the doctor has
                been successfully removed.
        Raises:
            ValueError: If doctor_id is not an integer or 
                        if no matching doctor is found.
        """
        
        try:
            doctor_id = int(doctor_id)
        except ValueError:
            raise ValueError('The ID must be a number')
        
        for doctor in self.doctors:
            if doctor.id == doctor_id:
                self.doctors.remove(doctor)
                return f'Doctor {doctor.name} {doctor.surname} with ID {doctor.id} removed'
        
        raise ValueError('Doctor not found')
    
    def schedule_appointment(self, patient, doctor, date, timeframe):
        if doctor in self.doctors:
            if patient in self.patients:
                if date in doctor.availabilities:
                    if doctor.availabilities[date[timeframe]]:
                        # Create new appointment
                        new_appointment = Appointment(patient, doctor, date)
                        self.appointments.append(new_appointment)
                        doctor.availabilities[date[timeframe]] = False
                        doctor.add_appointment(new_appointment)
                        patient.new_appointment(new_appointment)
                        
                        # Notifications
                        doctor_notification = Notification(f'Appointment scheduled for {date} at {timeframe(0)} for patient {patient.name} {patient.surname}')
                        doctor.add_notification(doctor_notification)
                        patient_notification = Notification(f'Appointment scheduled for {date} at {timeframe(0)} by Dr. {doctor.name} {doctor.surname}')
                        patient.add_notification(patient_notification)
                        return f'Appointment scheduled for {date}'
                    else:
                        return 'Doctor is not available on at that time'
                else:
                    return 'Doctor is not available on that date'
            else:
                return 'Patient not found'
        else:
            return 'Doctor not found'
    
    def cancel_appointment(patient, doctor, date):
        pass
    # activada por paciente o doctor
    # comprobar si la cita existe
    # si existe, eliminarla
    # notificar al paciente/doctor de la cancelación (diferentes mensajes, dependiendo de quién haya cancelado)
    
    def add_space(space):
        pass
    # comprobar si el espacio ya existe
    # si no existe, crear instancia y añadirlo a la lista
    
    def remove_space(space):
        pass
    # comprobar si el espacio existe
    # si existe, crear instancia y añadirlo a la lista