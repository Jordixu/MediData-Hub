from patient import Patient
from doctor import Doctor
from appointment import Appointment
from room import Room
from notification import Notification
import datetime as dt

class Hospital():
    """
    Represents a hospital with its patients, doctors, appointments and spaces. The functions may be implemented in Administrator class.
    """
    def __init__(self, name: str, location: str) -> None:
        """
        Initializes a new Hospital instance.
        Args:
            name (str): Name of the hospital.
            location (str): Location of the hospital.
        Attributes:
            name (str): Name of the hospital.
            location (str): Location of the hospital.
            patients (list): A list of patients.
            doctors (list): A list of doctors.
            appointments (list): A list of appointments.
            rooms (list): A list of hospital rooms or spaces.
            drugs (list): A list of medicines.
        """
        self.name = name
        self.location = location 
        self.patients = [] 
        self.doctors = []
        self.appointments = []
        self.rooms = []
        self.drugs = []
        
    def add_patient(self, patient_id: str, patient_name: str, patient_surname: str, patient_age: str, patient_gender: str, patient_weight: str, patient_height: str, patient_assigned_doctor: str, patient_status: str) -> str:
        """
        Adds a new patient to the hospital's records.
        Parameters:
            patient_id (str): Unique identifier for the patient, must be numeric.
            patient_name (str): First name of the patient.
            patient_surname (str): Surname of the patient.
            patient_age (str): Age of the patient, must be numeric and between 0 and 150.
            patient_gender (str): Gender of the patient.
            patient_weight (str): Weight of the patient in kilograms.
            patient_height (str): Height of the patient in centimeters.
            patient_assigned_doctor (str): Name of the doctor assigned to this patient.
            patient_status (str): Current status of the patient.
        Returns:
            str: A confirmation message indicating successful addition of the patient.
        Raises:
            ValueError: If the ID or age is not numeric, or if the age is invalid 
                        (e.g., negative or above 150), or if the patient already exists.
        """
        
        # We may change this for a dict input or a indirect input from another function
        
        # Check if input is valid
        try:
            patient_id = int(patient_id) # Check if the ID is a number
        except ValueError: # If not, raise an error
            raise ValueError("The ID must be a number") 
        
        try:
            patient_age = int(patient_age) # Check if the age is a number
        except ValueError: # If not, raise an error
            raise ValueError("The age must be a number") 
        
        if patient_age < 0 or patient_age > 150: # Check if the age is a valid number
            raise ValueError("Please, submit a valid age") # If not, raise an errror
        
        try:
            patient_weight = float(patient_weight) # Check if the weight is a number
        except ValueError: # If not, raise an error
            raise ValueError("The weight must be a number")
        
        if patient_weight < 0 or patient_weight > 1000: # Check if the weight is a valid number
            raise ValueError("Please, submit a valid weight")
        
        try:
            patient_height = float(patient_height) # Check if the height is a number
        except ValueError: # If not, raise an error
            raise ValueError("The height must be a number")
        
        if patient_height < 0 or patient_height > 300: # Check if the height is a valid number
            raise ValueError("Please, submit a valid height")
        
        for patient in self.patients: # Check if the patient already exists
            if patient.id == patient_id:
                raise ValueError('The ID is already in our system, perhaps there is a typo?') # If so, raise an error

        new_patient = Patient(patient_id, patient_name, patient_surname, patient_age, patient_gender, patient_weight, patient_height, patient_assigned_doctor, patient_status) # Create a new patient
        self.patients.append(new_patient) # Add the new patient to the list of patients
        return f'Patient {new_patient.name} {new_patient.surname} added' # Return a message confirming the addition of the new patient
            
    def remove_patient(self, patient_id: str) -> str: 
        """
        Removes a patient from the hospital's records by their unique identifier.
        Args:
            patient_id (str): The ID for the patient to be removed.
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

    def add_doctor(self, doctor_id: str, doctor_name: str, doctor_surname: str, doctor_age: str, doctor_gender: str, doctor_speciality: str, doctor_department: str, doctor_socialsecurity: str, doctor_salary: str) -> str:
        """
        Add a doctor to the hospital.
        This function attempts to parse and validate the parameters for a new doctor before
        creating and appending a new Doctor instance to the list of doctors.
        Parameters:
            doctor_id (str): The unique numeric identifier for the doctor.
            doctor_name (str): The first name of the doctor.
            doctor_surname (str): The last name of the doctor.
            doctor_age (str): The numeric age of the doctor (valid range: 0–150).
            doctor_gender (str): The gender of the doctor.
            doctor_speciality (str): The area of medical specialization.
            doctor_department (str): The department to which the doctor belongs.
            doctor_socialsecurity (str): The numeric social security number of the doctor.
            doctor_salary (str): The numeric salary of the doctor (non-negative).
        Returns:
            str: A message confirming the addition of the new doctor.
        Raises:
            ValueError: If any validation fails (e.g., non-numeric values, invalid age, 
                        negative salary) or if a doctor with the given ID already exists.
        """
        
        try:
            doctor_id = int(doctor_id)
        except ValueError:
            raise ValueError('The ID must be a number')
        
        try:
            doctor_age = int(doctor_age)
        except ValueError:
            raise ValueError('The age must be a number')
        
        if doctor_age < 0 or doctor_age > 150:
            raise ValueError('Please, submit a valid age')
        
        try:
            doctor_socialsecurity = int(doctor_socialsecurity)
        except ValueError:
            raise ValueError('The social security number must be a number')
        
        try:
            doctor_salary = float(doctor_salary)
        except ValueError:
            raise ValueError('The salary must be a number')
        
        if doctor_salary < 0:
            raise ValueError('Are really paying to work? Who are you, a student?') # easteregg
        
        for doctor in self.doctors:
            if doctor.id == doctor_id:
                raise ('Doctor already exists')
        
        new_doctor = Doctor(doctor_id, doctor_name, doctor_surname, doctor_age, doctor_gender, doctor_speciality, doctor_department, doctor_socialsecurity, doctor_salary)
        self.doctors.append(new_doctor)
        return f'Doctor {new_doctor.name} {new_doctor.surname} added'

    def remove_doctor(self, doctor_id: str) -> str:
        """
        Removes a doctor from the list by the provided ID.
        Args:
            doctor_id (str): The numeric identifier of the doctor to be removed.
        Returns:
            str: A confirmation message indicating that the doctor has been successfully removed.
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
            # Here we have to add the removal of appointments and send notifications to patients
            
        raise ValueError('Doctor not found')
    
    def schedule_appointment(self, patient: Patient, doctor: Doctor, date: date, timeframe: tuple) -> str:
        """
        Schedules an appointment for a patient with a specified doctor at a given date and timeframe.
        This method checks if the doctor is part of the hospital’s staff and ensures the requested date and timeframe are available. If availability is confirmed, it assigns an available room, creates a new appointment, and notifies both the doctor and patient.
        Args:
            patient (Patient): The patient requesting the appointment.
            doctor (Doctor): The doctor who will attend the appointment.
            date (date): The date of the requested appointment.
            timeframe (tuple): A specific time period within the given date.
        Returns:
            str: A message indicating the success or failure of the appointment scheduling process.
        """
        if doctor in self.doctors:
            if date in doctor.availabilities:
                if doctor.availabilities[date][timeframe]:
                    # Appointment
                    # Find an available room
                    for room in self.spaces:
                        if room.availability[date][timeframe]:
                            break
                    # Create the appointment
                    new_appointment = Appointment(date, timeframe, doctor, patient, room, status = True)
                    self.appointments.append(new_appointment)
                    doctor.availabilities[date][timeframe] = False # Change the availability of the doctor
                    room.availability[date][timeframe] = False # Change the availability of the room
                    doctor.add_appointment(new_appointment)
                    patient.new_appointment(new_appointment)
                    
                    # Notifications
                    doctor_notification = Notification(f'Appointment scheduled for {date} at {timeframe(0)} for patient {patient.name} {patient.surname}')
                    doctor.add_notification(doctor_notification)
                    patient_notification = Notification(f'Appointment scheduled for {date} at {timeframe(0)} by Dr. {doctor.name} {doctor.surname}')
                    patient.add_notification(patient_notification)
                    return f'Appointment scheduled for {date}'
                else:
                    return f'Dr. {doctor.surname} is not available on at that time, please choose another time frame'
            else:
                return f'Dr. {doctor.surname} is not available on that date, please choose another date'
        else:
            return 'Doctor not found, please introduce the correct ID' # We may take this out
    
    def cancel_appointment(self, patient: Patient, doctor: Doctor, date: str, timeframe: tuple) -> str:
        """
        Cancels an existing appointment for a given patient with a specified doctor, date, and timeframe.
        Parameters:
            patient (Patient): The patient for whom the appointment will be cancelled.
            doctor (Doctor): The doctor with whom the appointment was scheduled.
            date (str): The date of the appointment to be cancelled.
            timeframe (str): The specific timeframe (e.g., morning, afternoon) of the appointment to be cancelled.
        Returns:
            str: A message indicating whether the appointment was successfully cancelled or not.
        """
        
        for appointment in self.appointments:
            if appointment.patient == patient and appointment.doctor == doctor and appointment.date == date and appointment.timeframe == timeframe:
                self.appointments.remove(appointment)
                doctor.availabilities[date][appointment.timeframe] = True
                self.spaces[appointment.room].availability[date][appointment.timeframe] = True
                doctor.remove_appointment(appointment)
                patient.remove_appointment(appointment)
                
                # Notifications
                doctor_notification = Notification(f'Appointment cancelled for {date} at {appointment.timeframe(0)} for patient {patient.name} {patient.surname}')
                doctor.add_notification(doctor_notification)
                patient_notification = Notification(f'Appointment cancelled for {date} at {appointment.timeframe(0)} by Dr. {doctor.name} {doctor.surname}')
                patient.add_notification(patient_notification)
                return f'Appointment cancelled for {date}'
        return 'Appointment not found'
        
    # activada por paciente o doctor
    # comprobar si la cita existe
    # si existe, eliminarla
    # notificar al paciente/doctor de la cancelación (diferentes mensajes, dependiendo de quién haya cancelado)
    
    def add_room(self, room_number, floor_number, department_name):
        """
        Adds a new room to the hospital or returns that it already exists.
        Parameters:
            room_number (int or str): The identification number of the room.
            floor_number (int): The floor where the room is located.
            department_name (str): The name of the department the room belongs to.
        Returns:
            str: 'Room already exists' if the room is already in the hospital spaces, otherwise 'Room added'.
        """
        
        for room in self.spaces:
            if room.number == room_number and room.floor == floor_number and room.department == department_name:
                return 'Room already exists'
        self.spaces.append(room)
        return 'Room added'
    
    def remove_space(space):
        pass
    # comprobar si el espacio existe
    # si existe, crear instancia y añadirlo a la lista
    
    def add_medicine(self, medicine_name, comercial_name, active_ingredient, concentration, company, administration_route, price):
        pass # lo haremos cuando sepamos usar pandas
    
    
    
# ignore
def debugging(remove):
    global hospital
    hospital = Hospital('Hospital', 'Barcelona')
    hospital.add_patient(1, 'John', 'Doe', 25, 'M', 75, 180, 'Dr. Smith', 'Inpatient')
    if remove:
        hospital.remove_patient(1)

#debugging(True)