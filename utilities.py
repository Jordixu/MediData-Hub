import pandas as pd
import datetime as dt
import numpy as np
import random as rd
from faker import Faker

class Utilities:
    def __init__(self):
        self.fake = Faker(['en_US'])

    def load_from_csv(self, filename):
        try:
            df = pd.read_csv(filename)
            df = df.replace({float('nan'): None})
            if filename == './database/patients.csv' and 'birthday' in df.columns:
                df['birthday'] = df['birthday'].apply(
                    lambda x: dt.datetime.strptime(x.split()[0], '%Y-%m-%d').date() 
                    if pd.notnull(x) else None
                )
            return df.to_dict('records')
        except FileNotFoundError:
            print(f'File {filename} not found.')
            return []
        except pd.errors.EmptyDataError:
            print('No data found in the file')
            return []
        except Exception as e:
            print(f'An error occurred: {e}')
            return []
    
    def save_to_csv(self, data, filename):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, sep=',', encoding='utf-8')

    def update_database(self, hospital):    
        self.save_to_csv(
            [patient.get_all_attributes() for patient in hospital.patients], 
            './database/patients.csv'
            )
        self.save_to_csv(
            [doctor.get_all_attributes() for doctor in hospital.doctors], 
            './database/doctors.csv'
            )
        self.save_to_csv(
            [appointment.get_all_attributes() for appointment in hospital.appointments], 
            './database/appointments.csv'
            )
        self.save_to_csv(
            [room.get_all_attributes() for room in hospital.rooms], 
            './database/rooms.csv'
            )
        # save_to_csv(drugs_dict, './database/drugs.csv')
        
    def create_timeframe(self):
        timeframes = []
        start_time = dt.time(9, 0)
        end_time = dt.time(21, 0)
        current_time = start_time

        while current_time < end_time:
            next_time = (dt.datetime.combine(dt.date.today(), current_time) + dt.timedelta(hours=1)).time()
            timeframes.append((current_time.strftime("%H:%M"), next_time.strftime("%H:%M")))
            current_time = next_time
        return timeframes
        
    def create_week(self):
        week = []
        today = dt.date.today()
        for i in range(7):
            week.append(today + dt.timedelta(days=i))
        return week
    
    def create_schedule(self):
        schedule = {}
        for day in self.create_week():
            schedule[day] = {}
            for timeframe in self.create_timeframe():
                schedule[day][timeframe] = True
        return schedule

    def generate_patients(self, number_of_patients=100):
        patients = []
        patient_personal_ids = set()
        for x in range(number_of_patients):
            patient = {
                "personal_id": rd.randint(100000, 999999),
                "hospital_id": x,
                "password": self.fake.password(),
                "name": self.fake.name().split()[0],
                "surname": self.fake.name().split()[1],
                "birthday": self.fake.date_of_birth(minimum_age=16, maximum_age=120),
                "gender": rd.choice(["Male", "Female"]),
                "weight": rd.randint(50, 150) + round(rd.uniform(0, 1), 2),
                "height": rd.randint(150, 200) + round(rd.uniform(0, 1),2),
                "assigned_doctor_hid": None,
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
            
        self.save_to_csv(patients, "./database/patients.csv")

    def generate_doctors(self, number_of_doctors=100):
        doctors = [] 
        for x in range(number_of_doctors):
            doctors.append({
                "personal_id": rd.randint(100000, 999999),
                "hospital_id": x + 1000,
                "password": self.fake.password(),
                "name": self.fake.name().split()[0],
                "surname": self.fake.name().split()[1],
                "birthday": self.fake.date_of_birth(minimum_age=25, maximum_age=70),
                "gender": rd.choice(["Male", "Female"]),
                "speciality": rd.choice(["Cardiology", "Neurology", "Oncology", "Pediatrics", "Psychiatry", "Nephrology", "Gynecology", "Urology", "Dermatology", "Endocrinology"]),
                "department": rd.choice(["ER", "Surgery", "Internal Medicine", "Pediatrics", "Psychiatry", "Oncology", "Cardiology", "Neurology", "Gynecology", "Urology"]),
                "socialsecurity": self.fake.ssn(),
                "salary": rd.randint(40000, 100000) + round(rd.uniform(0, 1), 2),
                "assigned_patients": None,
                "notifications": None,
                "availability": self.create_schedule(),
                "appointments": None
            })
        self.save_to_csv(doctors, "./database/doctors.csv")

    def generate_rooms(self, number_of_floors=6, rooms_per_floor=20):
        rooms = []
        for number in range(rooms_per_floor):
            for floor in range(number_of_floors):
                rooms.append({
                    "number": number,
                    "floor": floor,
                    "department": rd.choice(["ER", "Surgery", "Internal Medicine", "Pediatrics", "Psychiatry", "Oncology", "Cardiology", "Neurology", "Gynecology", "Urology"]),
                })
        self.save_to_csv(rooms, "./database/rooms.csv")

    def generate_appointments(self, number_of_appointments=100):        
        # Load previously generated data
        doctors = pd.read_csv("./database/doctors.csv")
        patients = pd.read_csv("./database/patients.csv")
        rooms = pd.read_csv("./database/rooms.csv")

        doctor_ids = doctors["hospital_id"].tolist()
        patient_ids = patients["hospital_id"].tolist()
        room_numbers = rooms["number"].tolist()

        appointments = []
        for x in range(number_of_appointments):
            appointments.append({
                "appointment_id": x,
                "doctor_hid": rd.choice(doctor_ids),
                "patient_hid": rd.choice(patient_ids),
                "date": rd.choice(self.create_week()),
                "timeframe": rd.choice(self.create_timeframe()),
                "room_number": rd.choice(room_numbers),
                "status": rd.choice(["Scheduled", "Cancelled"]),
                "diagnosis_id": None,
                "medication_id": None,
            })
        self.save_to_csv(appointments, "./database/appointments.csv")

    def generate_drugs(self, number_of_drugs = 100): # Aun no se bien bien los atributos de los medicamentos
        drugs = []
        for x in range(number_of_drugs):
            drugs.append({
                "medication_id": x,
                "name": self.fake.word(),
                "description": self.fake.text(max_nb_chars=200),
                "side_effects": self.fake.text(max_nb_chars=200),
                "dosage": self.fake.text(max_nb_chars=200),
                "prescription": None,
            })
        self.save_to_csv(drugs, "./database/drugs.csv")
