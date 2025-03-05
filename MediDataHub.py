import datetime as dt
from typing import Union
from patient import Patient
from doctor import Doctor
from appointment import Appointment
from room import Room
from notification import Notification
from utilities import Utilities
from drug import Drug
from diagnosis import Diagnosis
from prescription import Prescription

class Hospital:

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
        self.diagnoses = {}
        self.prescriptions = {}
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
                try:
                    appointment['room_number'] = int(appointment['room_number'])
                except TypeError:
                    appointment['room_number'] = 'N/A'
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
                notification['datetime'] = notification['datetime'].to_pydatetime()
                # print(type(notification['datetime']))
                new_notification = Notification(**notification)
                self.notifications[new_notification.get('notification_id')] = new_notification
                # print("Notification:", new_notification)
        except FileNotFoundError as exc:
            raise FileNotFoundError('No notifications found in the database') from exc
        except TypeError as e:
            print(f"Incorrect type: {e}")
            
        try:
            for drug in self.utility.load_from_csv('./database/drugs.csv'):
                new_drug = Drug(**drug)
                self.drugs[new_drug.get('drug_id')] = new_drug
        except FileNotFoundError as exc:
            raise FileNotFoundError('No drugs found in the database') from exc
        except TypeError as e:
            print(f"Incorrect type: {e}")
            
        try:
            for diagnosis in self.utility.load_from_csv('./database/diagnoses.csv'):
                new_diagnosis = Diagnosis(**diagnosis)
                self.diagnoses[new_diagnosis.get('diagnosis_id')] = new_diagnosis
        except FileNotFoundError as exc:
            raise FileNotFoundError('No diagnoses found in the database') from exc
        except TypeError as e:
            print(f"Incorrect type: {e}")
        
        try:
            for prescription in self.utility.load_from_csv('./database/prescriptions.csv'):
                self.prescriptions[prescription['prescription_id']] = prescription
                print(prescription)
        except FileNotFoundError as exc:
            raise FileNotFoundError('No prescriptions found in the database') from exc
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

    def remove_patient(self, patient_hospital_id: Union[int, str]) -> str:
        """
        Removes a patient from the system based on their ID.
        
        Args:
            patient_hospital_id (Union[int, str]): The ID of the patient to remove.
        
        Raises:
            ValueError: If the patient is not found in the system.
        """
        patient_hospital_id = self.utility.validate_and_cast_value(patient_hospital_id, int, custom_message_incorrect_type="The ID must be a number.")
        
        if patient_hospital_id in self.patients.keys():
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
        if 'hospital_id' in kwargs:
            kwargs['hospital_id'] = self.utility.validate_and_cast_value(kwargs['hospital_id'], int, 0)
        kwargs['socialsecurity'] = self.utility.validate_and_cast_value(kwargs['socialsecurity'], str)
        kwargs['salary'] = self.utility.validate_and_cast_value(kwargs['salary'], float, 0)
        
        if not (dt.date(1900, 1, 1) <= kwargs['birthday'] <= dt.date(2005, 1, 1)):
            raise ValueError("You must be born between 1900 and 2005 to work here.")
        
        if any(d.get_protected_attribute("personal_id") == kwargs['personal_id'] for d in self.doctors.values()):
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

        if doctor_id in self.doctors.keys():
            del self.doctors[doctor_id]
            return

        raise ValueError('Doctor not found.')
    
    def add_drug(self, **kwargs) -> None:
        """
        Adds a new drug to the system.
        
        Args:
            name (str): The name of the drug.
            commercial_name (str): The commercial name of the drug.
            price (float): The price of the drug.
            company (str): The company that produces the drug.
            prescription (bool): Whether the drug requires a prescription.
        """
        for drug in self.drugs.values():
            if drug.get('name') == kwargs['name']:
                raise ValueError('Drug already exists.')
            
        for key in ['name', 'commercial_name', 'price', 'company', 'prescription']:
            if key not in kwargs:
                raise ValueError(f"Missing required field: {key}")
        
        kwargs['price'] = self.utility.validate_and_cast_value(kwargs['price'], float, 0)
        kwargs['prescription'] = self.utility.validate_and_cast_value(kwargs['prescription'], bool)
        
        if 'drug_id' not in kwargs:
            drug_id = max(self.drugs.keys(), default=0) + 1
            kwargs['drug_id'] = drug_id
            
        new_drug = Drug(**kwargs)
        self.drugs[drug_id] = new_drug
    
    def remove_drug(self, drug_id: int) -> None:
        """
        Removes a drug from the system.
        
        Args:
            drug_id (int): The ID of the drug to remove.
        """
        drug_id = self.utility.validate_and_cast_value(drug_id, int, custom_message_incorrect_type="The ID must be a number.")
        
        if drug_id in self.drugs.keys():
            del self.drugs[drug_id]
            return
        
        raise ValueError('Drug not found.')

    def close_room(self, room_number: int) -> None:
        """
        Closes a room and reschedules all its appointments to available rooms.
        
        Args:
            room_number (int): The number of the room to close.
            
        Raises:
            ValueError: If the room does not exist.
        """
        # Check if the room exists
        room = self.rooms.get(room_number)
        if not room:
            raise ValueError(f"Room {room_number} not found.")
        
        # Get all appointments associated with this room
        affected_appointments = []
        for appointment in self.appointments.values():
            if appointment.get('room_number') == room_number and appointment.get('status') == 'Scheduled':
                affected_appointments.append(appointment)
        
        # Close the room by setting all availability to False
        for date in room.display_schedule():
            for timeframe in room.display_schedule()[date]:
                if room.check_availability(date, timeframe):
                    room.change_availability(date, timeframe)
        
        # Reschedule all affected appointments
        for appointment in affected_appointments:
            appt_id = appointment.get('appointment_id')
            doctor_id = appointment.get('doctor_hid')
            patient_id = appointment.get('patient_hid')
            date = appointment.get('date')
            timeframe = appointment.get('timeframe')
            
            # Try to find an available room
            new_room_found = False
            for new_room in self.rooms.values():
                # Skip the closed room and check others
                if new_room.get('number') == room_number:
                    continue
                    
                # If an available room is found, reschedule the appointment
                if new_room.check_availability(date, timeframe):
                    appointment.change_room(new_room.get('number'))
                    new_room.change_availability(date, timeframe)
                    new_room_found = True
                    
                    # Notify patient and doctor about room change
                    self.send_notification(
                        patient_id, 
                        0,  # System notification
                        'Room Change', 
                        'Information', 
                        f"Your appointment on {date} at {timeframe[0]} has been moved to room {new_room.get('number')} due to maintenance."
                    )
                    
                    self.send_notification(
                        doctor_id, 
                        0,  # System notification
                        'Room Change', 
                        'Information', 
                        f"Your appointment with patient {patient_id} on {date} at {timeframe[0]} has been moved to room {new_room.get('number')} due to maintenance."
                    )
                    
                    break

            # If no available room is found, cancel the appointment
            if not new_room_found:
                appointment.change_status('Cancelled')
                
                # Notify patient and doctor about cancellation
                self.send_notification(
                    patient_id, 
                    0,  # System notification
                    'Appointment Cancelled', 
                    'Cancellation', 
                    f"Your appointment on {date} at {timeframe[0]} has been cancelled due to room {room_number} closure and no available alternatives."
                )
                
                self.send_notification(
                    doctor_id, 
                    0,  # System notification
                    'Appointment Cancelled', 
                    'Cancellation', 
                    f"Your appointment with patient {patient_id} on {date} at {timeframe[0]} has been cancelled due to room {room_number} closure."
                )

    def open_room(self, room_number: int) -> None:
        """
        Opens a room and sets all its availability to True.
        
        Args:
            room_number (int): The number of the room to open.
            
        Raises:
            ValueError: If the room does not exist.
        """
        room = self.rooms.get(room_number)
        if not room:
            raise ValueError(f"Room {room_number} not found.")
        
        # Check if the room already has any available time slots
        for date in room.display_schedule():
            for timeframe in room.display_schedule()[date]:
                if room.check_availability(date, timeframe):
                    raise ValueError(f"Room {room_number} is already open with available time slots.")
        
        for date in room.display_schedule():
            for timeframe in room.display_schedule()[date]:
                room.change_availability(date, timeframe)
        
    def request_appointment(self, patient_hid: int, doctor_hid: int) -> None:
        doctor = self.doctors[doctor_hid]
        if not doctor:
            raise ValueError('Doctor not found')
        
        patient = self.patients[patient_hid]
        if not patient:
            raise ValueError('Patient not found')

        appointment_id = max(self.appointments.keys(), default=0) + 1
        appointment = Appointment(appointment_id=int(appointment_id), patient_hid=patient_hid, doctor_hid=doctor_hid, date = 'N/A', timeframe='N/A', room_number='N/A', status='Pending')
        self.appointments[appointment.get('appointment_id')] = appointment
        doctor.add_appointment(appointment.get('appointment_id'))
        patient.add_appointment(appointment.get('appointment_id'))
        return appointment_id

    def schedule_appointment(self, appointment_id: int, date: dt.date, timeframe: tuple) -> None:
        """
        Schedules an appointment between a patient and a doctor.
        
        Args:
            patient_hid (int): The hospital ID of the patient.
            doctor_hid (int): The hospital ID of the doctor.
            date (dt.date): The date of the appointment.
            timeframe (tuple): The timeframe of the appointment.
        """
        doctor = self.appointments[appointment_id].get('doctor_hid')
        patient = self.appointments[appointment_id].get('patient_hid')
        appointment = self.appointments[appointment_id]
        
        if not self.doctors[doctor].check_availability(date, timeframe):
            # print(doctor.get('availability'))
            # print(date, timeframe)
            # print(type(doctor.get('availability')[date]))
            # print(type(doctor.get('availability')[date][timeframe]))
            # print(type(date))
            raise ValueError('Doctor not available at that time')

        try:
            for room in self.rooms.values():
                if room.check_availability(date, timeframe):
                    self.doctors[doctor].change_availability(date, timeframe)
                    room.change_availability(date, timeframe)
                    appointment.change_status('Scheduled')
                    appointment.change_datetime(date, timeframe)
                    appointment.change_room(int(room.get('number')))
                    # print(room.get('number'))
                    self.send_notification(patient, doctor, 'Appointment Scheduled', 'Appointment', f'Your appointment with Dr. {self.doctors[doctor].get_protected_attribute("surname")} has been scheduled for {str(date)} at {str(timeframe[0])}')
                    return
                else:
                    continue
            raise ValueError('No available rooms for the appointment')
        except Exception as exc:
            print(exc)

    def reschedule_appoitment(self, appointment_id: int, date: dt.date, timeframe: tuple, room_number: int = None) -> None:
        """
        Reschedules an appointment between a patient and a doctor.
        
        Args:
            appointment_id (int): The ID of the appointment to reschedule.
            date (dt.date): The new date of the appointment.
            timeframe (tuple): The new timeframe of the appointment.
            room_number (int): The new room number for the appointment.
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
        
        if not doctor.check_availability(date, timeframe):
            raise ValueError('Doctor not available at that time.')
        
        if room_number:
            room = self.rooms.get(room_number)
            if not room:
                raise ValueError(f"Room {room_number} not found.")
            
            if not room.check_availability(date, timeframe):
                raise ValueError(f"Room {room_number} not available at that time.")
        
        appointment.change_datetime(date, timeframe)
        if room_number:
            appointment.change_room(room_number)
        
        self.send_notification(patient.get_protected_attribute('hospital_id'), doctor.get_protected_attribute('hospital_id'), 'Appointment Rescheduled', 'Appointment', f'Your appointment with Dr. {doctor.get_protected_attribute("surname")} has been rescheduled for {str(date)} at {str(timeframe[0])}')
        return

    def cancel_appointment(self, appointment_id: int, sender: str) -> str:
        """
        Cancels an appointment between a patient and a doctor.
        
        Args:
            appointment_id (int): The ID of the appointment to cancel.
        
        Returns:
            str: A confirmation message or an error message.
        """
        appointment_id = self.utility.validate_and_cast_value(appointment_id, int, custom_message_incorrect_type="The ID must be a number.")
        
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
        
        if sender == 'doctor':
            self.send_notification(patient.get_protected_attribute('hospital_id'), doctor.get_protected_attribute('hospital_id'), 'Appointment Cancelled', 'Cancellation', f'Your appointment with Dr. {doctor.get_protected_attribute("surname")} has been cancelled.')
            return
        elif sender == 'patient':
            self.send_notification(doctor.get_protected_attribute('hospital_id'), patient.get_protected_attribute('hospital_id'), 'Appointment Cancelled', 'Cancellation', f'Your appointment with {patient.get_protected_attribute("name")} {patient.get_protected_attribute("surname")} has been cancelled.')
            return
        elif sender == 'admin':
            self.send_notification(patient.get_protected_attribute('hospital_id'), doctor.get_protected_attribute('hospital_id'), 'Appointment Cancelled', 'Cancellation', f'Your appointment with Dr. {doctor.get_protected_attribute("surname")} has been cancelled.')
            return
        else:
            raise ValueError('Sender not found')

    def send_notification(self, receiver_hid: int, sender_hid: int, title:str, type: str, message: str, appointment_id: int = None) -> None:
        """
        Sends a notification from the sender to the receiver with the given message.
        
        Args:
            receiver_hid (int): The recipient of the notification.
            sender_hid (int): The sender of the notification.
            message (str): The content of the notification message.
        
        Returns:
            None
        """
        dat = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dat = dt.datetime.strptime(dat, '%Y-%m-%d %H:%M:%S')
        
        notification_id = max(self.notifications.keys(), default=0) + 1
        new_notif = Notification(notification_id, title, dat, sender_hid, receiver_hid, type, message, appointment_id=appointment_id)
        self.notifications[notification_id] = new_notif
        
        if receiver_hid in self.patients:
            self.patients[receiver_hid].add_notification(notification_id)
        elif receiver_hid in self.doctors:
            self.doctors[receiver_hid].add_notification(notification_id)
        else:
            raise ValueError('Receiver not found')
    
    def remove_notification(self, notification_id):
        """
        Removes a notification from the system.
        
        Args:
            notification_id (int): The ID of the notification to remove.
        """
        notification_id = self.utility.validate_and_cast_value(notification_id, int, custom_message_incorrect_type="The ID must be a number.")
        
        if notification_id in self.notifications.keys():
            del self.notifications[notification_id]
            return
        
        raise ValueError('Notification not found.')

    def create_diagnosis(self, title: str, description: str, treatment: str, appointment_id: int, doctor_hid: int, patient_hid: int) -> None:
        # try:                
            # Generate a new diagnosis ID
            diagnosis_id = max(self.diagnoses.keys(), default=0) + 1
            # print(type(self.diagnoses))
            
            # Create diagnosis
            diagnosis = Diagnosis(diagnosis_id, title, appointment_id, doctor_hid, patient_hid, treatment, dt.date.today(), description)
            
            # Add to hospital diagnoses
            self.diagnoses[diagnosis_id] = diagnosis
            
            # Add diagnosis to patient's record
            patient = self.patients[patient_hid]
            patient.add_diagnosis(diagnosis_id)
            
            doctor = self.doctors[doctor_hid]
            doctor.add_diagnosis(diagnosis_id)
            
            return diagnosis_id
            
        # except Exception as e:
        #     print(f"Error creating diagnosis: {e}")
        #     raise
    
    def prescribe_medication(self, patient_hid, doctor_hid, diagnosis_id, medication, appointment_id) -> None:
        try:
            # Create a prescription for each medication
            for drug_id, dosage in medication.items():
                # Generate a new prescription ID
                prescription_id = max(self.prescriptions.keys(), default=0) + 1
                
                # Create prescription
                new_prescription = Prescription(prescription_id, drug_id, dosage, doctor_hid, patient_hid, appointment_id, diagnosis_id)
                
                # Add to hospital prescriptions
                self.prescriptions[prescription_id] = new_prescription
                
                # Add prescription to patient's record
                patient = self.patients[patient_hid]
                patient.add_prescription(prescription_id)
                
                doctor = self.doctors[doctor_hid]
                doctor.add_prescription(prescription_id)
                
        except Exception as e:
            print(f"Error creating prescriptions: {e}")
            raise