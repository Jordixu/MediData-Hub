from faker import Faker
import random as rd
from utilities import Data

def generate_fake_data():
    fake = Faker(['en_US'])

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
            "appointments": None
        })
        
    rooms = []
    for number in range(21):
        for floor in range(6):
            rooms.append({
                "number": number,
                "floor": floor,
                "department": rd.choice(["ER", "Surgery", "Internal Medicine", "Pediatrics", "Psychiatry", "Oncology", "Cardiology", "Neurology", "Gynecology", "Urology"]),
            })
            
    

    Data.save_to_csv(patients, "./database/patients.csv")
    Data.save_to_csv(doctors, "./database/doctors.csv")