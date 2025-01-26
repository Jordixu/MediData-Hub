from faker import Faker
import random as rd
from utilities import Data
import datetime as dt
from utilities import Datetime
import pandas as pd

fake = Faker(['en_US'])
class DataGenerator:
    """
    Class to generate random data for the hospital database. All data is saved to CSV files. All methods are static.
    
    Methods:
        generate_patients(): Generates random patient data.
        generate_doctors(): Generates random doctor data.
        generate_rooms(): Generates random room data.
        generate_appointments(): Generates random appointment data.
        generate_drugs(): Generates random drug data.
    """

    @staticmethod
    def generate_patients():
        patients = []
        patient_personal_ids = set()
        for x in range(101):
            patient = {
                "personal_id": rd.randint(100000, 999999),
                "hospital_id": x,
                "password": fake.password(),
                "name": fake.name().split()[0],
                "surname": fake.name().split()[1],
                "birthday": fake.date_of_birth(minimum_age=16, maximum_age=120),
                "gender": rd.choice(["Male", "Female"]),
                "weight": rd.randint(50, 150) + round(rd.uniform(0, 1), 2),
                "height": rd.randint(150, 200) + round(rd.uniform(0, 1),2),
                "assigned_doctor": None,
                "status": rd.choices(["Inpatient", "Outpatient", "Emergency"], weights=(0.15, 0.8, 0.05), k=1)[0],
                "appointments": None,
                "medications": None,
                "allergies": None,
                "diagnoses": None,
            }
            
            # To ensure no duplicate personal ids
            if patient["personal_id"] in patient_personal_ids:
                continue
            
            patient_personal_ids.add(patient["personal_id"])
            patients.append(patient)
            
        Data.save_to_csv(patients, "./database/patients.csv")


    @staticmethod
    def generate_doctors():
        doctors = [] 
        for x in range(101):
            doctors.append({
                "personal_id": rd.randint(100000, 999999),
                "hospital_id": x + 1000,
                "password": fake.password(),
                "name": fake.name().split()[0],
                "surname": fake.name().split()[1],
                "birthday": fake.date_of_birth(minimum_age=25, maximum_age=70),
                "gender": rd.choice(["Male", "Female"]),
                "speciality": rd.choice(["Cardiology", "Neurology", "Oncology", "Pediatrics", "Psychiatry", "Nephrology", "Gynecology", "Urology", "Dermatology", "Endocrinology"]),
                "department": rd.choice(["ER", "Surgery", "Internal Medicine", "Pediatrics", "Psychiatry", "Oncology", "Cardiology", "Neurology", "Gynecology", "Urology"]),
                "socialsecurity": fake.ssn(),
                "salary": rd.randint(40000, 100000) + round(rd.uniform(0, 1), 2),
                "assigned_patients": None,
                "notifications": None,
                "availability": Datetime.create_schedule(),
                "appointments": None
            })
        Data.save_to_csv(doctors, "./database/doctors.csv")


    @staticmethod
    def generate_rooms():
        rooms = []
        for number in range(21):
            for floor in range(6):
                rooms.append({
                    "number": number,
                    "floor": floor,
                    "department": rd.choice(["ER", "Surgery", "Internal Medicine", "Pediatrics", "Psychiatry", "Oncology", "Cardiology", "Neurology", "Gynecology", "Urology"]),
                })
        Data.save_to_csv(rooms, "./database/rooms.csv")


    @staticmethod
    def generate_appointments():        
        # Load previously generated data
        doctors = pd.read_csv("./database/doctors.csv")
        patients = pd.read_csv("./database/patients.csv")
        rooms = pd.read_csv("./database/rooms.csv")

        doctor_ids = doctors["hospital_id"].tolist()
        patient_ids = patients["hospital_id"].tolist()
        room_numbers = rooms["number"].tolist()

        appointments = []
        for x in range(100):
            appointments.append({
                "appointment_id": x,
                "doctor": rd.choice(doctor_ids),
                "patient": rd.choice(patient_ids),
                "date": rd.choice(Datetime.create_week()),
                "timeframe": rd.choice(Datetime.create_timeframe()),
                "room": rd.choice(room_numbers),
                "status": rd.choice(["Scheduled", "Cancelled"]),
                "diagnosis": None,
                "medication": None,
            })
        Data.save_to_csv(appointments, "./database/appointments.csv")
        
    @staticmethod
    def generate_drugs(): # Aun no se bien bien los atributos de los medicamentos
        drugs = []
        for x in range(100):
            drugs.append({
                "medication_id": x,
                "name": fake.word(),
                "description": fake.text(max_nb_chars=200),
                "side_effects": fake.text(max_nb_chars=200),
                "dosage": fake.text(max_nb_chars=200),
                "prescription": None,
            })
        Data.save_to_csv(drugs, "./database/drugs.csv")