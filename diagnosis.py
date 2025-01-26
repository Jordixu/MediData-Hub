class Diagnosis():
    """
    Represents a diagnosis for a patient.
    
    Attributes:
        diagnosis_id (int): The ID of the diagnosis.
        title (str): The title of the diagnosis.
        appointment_id (int): The ID of the appointment associated with the diagnosis.
        doctor_hid (int): The ID of the doctor who diagnosed the patient.
        patient_hid (int): The ID of the patient diagnosed.
        description (str): The description of the diagnosis.
        treatment (str): The treatment prescribed for the diagnosis.
    """
    def __init__(self, id: int, title: str, appointment_id: int, doctor_hid: int, patient_hid: int, treatment, description = None):
        self.diagnosis_id = id
        self.title = title
        self.__appointment_id = appointment_id
        self.__doctor_hid = doctor_hid
        self.__patient_hid = patient_hid
        self.__description = description
        self.__treatment = treatment # medication, surgery, therapy, etc. POR DETERMINAR
        
    def __str__(self):
        return f'{self.title} {self.__description} {self.__treatment}'
    
    # FALTA