from person import Person
from datetime import date

class Patient(Person):
    """
    Represents a patient in a hospital.
    
    Attributes (not form person):
        weight (float): The weight of the patient.
        height (float): The height of the patient.
        assigned_doctor (Doctor): The doctor assigned to the patient.
        status (str): The status of the patient (Inpatient, Outpatient, Emergency).
        medications (list): A list of medications prescribed to the patient.
        allergies (list): A list of allergies the patient has.
        diagnoses (list): A list of diagnoses the patient has.
        notifications (list): A list of notifications the patient has received.
    
    Methods:
        add_diagnosis(int): Adds a diagnosis to the patient.
        remove_diagnosis(diagnosis_date, last_diagnosis): Removes a diagnosis from the patient.
        add_medication(medication): Adds a medication to the patient.
        remove_medication(medication, last_medication): Removes a medication from the patient.
        add_allergy(allergy): Adds an allergy to the patient.
        remove_allergy(allergy, last_allergy): Removes an allergy from the patient.
    """
    
    def __init__(self, 
            personal_id: int, 
            hospital_id: int,
            password: str, 
            name: str, 
            surname: str, 
            birthday: date, 
            gender: str, 
            weight: float, 
            height: float, 
            assigned_doctor_hid: int = None, 
            status: str = 'Outpatient', 
            appointments: list = None, 
            medications: list = None, 
            allergies: list = None, 
            diagnoses: list = None, 
            notifications: list = None
            ) -> None:
        """
        Initialize a new Patient instance.
        Args:
            personal_id (int): The personal ID of the patient.
            hospital_id (int): The hospital ID of the patient.
            password (str): The password for the patient's account.
            name (str): The first name of the patient.
            surname (str): The surname of the patient.
            birthday (date): The birth date of the patient.
            gender (str): The gender of the patient.
            weight (float): The weight of the patient.
            height (float): The height of the patient.
            assigned_doctor_hid (int, optional): The doctor assigned to the patient. Defaults to None.
            status (str, optional): The status of the patient (Inpatient, Outpatient, Emergency). Defaults to 'Outpatient'.
            appointments (list, optional): The list of appointments for the patient. Defaults to None.
            medications (list, optional): The list of medications for the patient. Defaults to None.
            allergies (list, optional): The list of allergies for the patient. Defaults to None.
            diagnoses (list, optional): The list of diagnoses for the patient. Defaults to None.
            notifications (list, optional): The list of notifications for the patient. Defaults to None.
        """
        
        super().__init__(personal_id, hospital_id, password, name, surname, birthday, gender, appointments, notifications)
        self.__weight = weight
        self.__height = height
        self.__status = status # Inpatient, Outpatient, Emergency
        self.__prescriptions = medications if medications is not None else []
        self.__diagnoses = diagnoses if diagnoses is not None else []

        
    def __str__(self):
        """REturns a string representation of the patient.
        
        Returns:
            str: The string representation of the patient.
        """
        return f'Patient {self._name} {self._surname} {self._personal_id} {self._password} {self._birthday} {self.__prescriptions} {self.__diagnoses} {self._notifications} {self.__weight} {self.__height} {self.__status} {self._appointments}'
        
    def add_diagnosis(self, diagnosis_id) -> None:
        """Adds a diagnosis to the patient.
        
        Args:
            diagnosis_id (int): The diagnosis ID to add.
        """
        self.__diagnoses.append(diagnosis_id)
        
    def remove_diagnosis(self, diagnosis_id) -> None:
        """Removes a diagnosis from the patient.
        
        Args:
            diagnosis_id (int): The diagnosis ID to remove.
        """
        try:
            del self.__diagnoses[diagnosis_id]
        except IndexError:
            print('Diagnosis not found')
        
    def add_presciption(self, prescription_id) -> None:
        if prescription_id not in self.__prescriptions.keys():
            self.__prescriptions.append(prescription_id)
        else:
            raise ValueError('Prescription already exists')
        
    def remove_prescription(self, prescription_id) -> None:
        try:
            del self.__prescriptions[prescription_id]
        except IndexError:
            print('Prescription not found')