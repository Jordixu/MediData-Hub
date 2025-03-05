from foundation import Foundation

class Prescription(Foundation):
    def __init__(self, prescription_id: int, drug_id: int, dosage: float, doctor_hid: int, patient_hid: int, appointment_id: int, diagnosis_id: int, status: str = "Active") -> None:
        super().__init__()
        self.__prescription_id = prescription_id
        self.__drug_id = drug_id
        self.__dosage = dosage
        self.__doctor_hid = doctor_hid
        self.__patient_hid = patient_hid
        self.__appointment_id = appointment_id
        self.__diagnosis_id = diagnosis_id
        self.__status = status
        
    def __str__(self):
        return f'{self.__prescription_id} {self.__drug_id} {self.__dosage} {self.__doctor_hid} {self.__patient_hid} {self.__appointment_id}'
    
    def autocomplete(self) -> None:
        self.__status = 'Inactive'