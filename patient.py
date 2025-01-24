from person import Person
from notification import Notification
from doctor import Doctor
from datetime import date

class Patient(Person):
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
            assigned_doctor: Doctor = None, 
            status: str = 'Outpatient', 
            appointments: dict = None, 
            medications: list = None, 
            allergies: list = None, 
            diagnoses: list = None, 
            notifications: list = None
            ) -> None:
        
        super().__init__(personal_id, hospital_id, password, name, surname, birthday, gender)
        self.weight = weight
        self.height = height
        self.assigned_doctor = assigned_doctor
        self.status = status # Inpatient, Outpatient, Emergency
        self.__appointments = appointments if appointments is not None else {}
        self.__medications = medications if medications is not None else []
        self.__allergies = allergies if allergies is not None else []
        self.__diagnoses = diagnoses if diagnoses is not None else []
        self.__notifications = notifications if notifications is not None else []
        
    def __str__(self):
        return f'Patient {self.name} {self.surname} {self._password}'
        
    def get(self, attribute: str) -> str:
        try:
            return getattr(self, attribute)
        except AttributeError:
            return 'Attribute not found'
        except TypeError:
            return 'Invalid value'
        except:
            return 'An error occurred'
    
    def add_appointment(self, appointment) -> None:
        self.__appointments.append(appointment)
        
    def remove_last_appointment(self, appointment, last_appointment: bool) -> None:
        if last_appointment:
            self.__appointments.pop()
        else:
            self.__appointments = [app for app in self.__appointments if app != appointment]
        
    def add_diagnosis(self, diagnostic) -> None:
        self.__diagnoses.append(diagnostic)
        
    def remove_diagnosis(self, date, last_diagnosis: bool) -> None:
        if last_diagnosis:
            self.__diagnoses.pop()
        else:
            self.__diagnoses = [diagnosis for diagnosis in self.__diagnoses if diagnosis.date != date]
        
    def add_medication(self, medication) -> None:
        self.__medications.append(medication)
        
    def remove_medication(self, medication, last_medication: bool) -> None:
        if last_medication:
            self.__medications.pop()
        else:
            self.__medications = [med for med in self.__medications if med != medication]
        
    def add_allergy(self, allergy) -> None:
        self.__allergies.append(allergy)
        
    def remove_allergy(self, allergy, last_allergy: bool) -> None:
        if last_allergy:
            self.__allergies.pop()
        else:
            self.__allergies = [al for al in self.__allergies if al != allergy]
        
    def change_assigned_doctor(self, doctor: Doctor) -> None:
        self._assigned_doctor = doctor
        
    def change_status(self, status: str) -> None:
        self._status = status