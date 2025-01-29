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
            df = pd.read_csv(filename, sep=';').replace({float('nan'): None})
            return self.process_dataframe(df)
        except FileNotFoundError:
            print(f'File {filename} not found.')
            return []
        except pd.errors.EmptyDataError:
            print('No data found in the file')
            return []

    def process_dataframe(self, df):
        # Process special formats first
        for column in df.columns:
            if column in ['birthday', 'date']:
                df[column] = df[column].apply(self.process_date)
            elif column == 'timeframe':
                df[column] = df[column].apply(self.process_timeframe)
            else:
                df[column] = df[column].apply(self.auto_convert)

        return df.to_dict('records')

    def process_date(self, value):
        if pd.isna(value):
            return None
        try:
            return dt.datetime.strptime(value.split()[0], '%Y-%m-%d').date()
        except (ValueError, AttributeError):
            return None

    def process_timeframe(self, value):
        if pd.isna(value):
            return None
        try:
            return tuple(value.split('-')) if '-' in value else value
        except AttributeError:
            return None

    def auto_convert(self, value):
        """
        Convert a value to an appropriate data type.

        Args:
            value: The value to be converted.

        Returns:
            The converted value, which can be an int, float, bool, list of ints, or the original string.
        """
        if pd.isna(value):
            return None

        # Try to convert to int, float, bool, or keep as string
        if isinstance(value, str):
            value = value.strip()  # Remove leading/trailing whitespace
            if value.lower() in ('true', 'false'):  # Handle booleans
                return value.lower() == 'true'
            try:
                if '.' in value:  # Check if it's a float
                    return float(value)
                elif ',' in value:  # Check if it's a list of integers
                    result = [int(v.strip()) for v in value.split(',') if v.strip().isdigit()]
                    return result
                else:  # Check if it's an integer
                    return int(value)
            except ValueError:
                pass  # If conversion fails, keep as string

        return value
    
    def save_to_csv(self, data, filename):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, sep=';', encoding='utf-8')

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

    def random_datas(
        self, 
        number_of_patients=100, 
        number_of_doctors=100, 
        number_of_floors=6, 
        rooms_per_floor=20, 
        number_of_appointments=100, 
        number_of_drugs=100
    ):
        # Generate patients
        patients = []
        patient_personal_ids = set()
        for x in range(number_of_patients):
            pid = rd.randint(100000, 999999)
            if pid not in patient_personal_ids:
                patient_personal_ids.add(pid)
                patients.append({
                    "personal_id": pid,
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
                    "appointments": [],
                })

        # Generate doctors
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
                "speciality": rd.choice([
                    "Cardiology","Neurology","Oncology","Pediatrics","Psychiatry",
                    "Nephrology","Gynecology","Urology","Dermatology","Endocrinology"
                ]),
                "department": rd.choice([
                    "ER","Surgery","Internal Medicine","Pediatrics","Psychiatry","Oncology",
                    "Cardiology","Neurology","Gynecology","Urology"
                ]),
                "socialsecurity": self.fake.ssn(),
                "salary": rd.randint(40000, 100000) + round(rd.uniform(0, 1), 2),
                "availability": self.create_schedule(),
                "appointments": []
            })

        rooms = []
        for floor in range(number_of_floors):
            for number in range(rooms_per_floor):
                rooms.append({
                    "number": floor * 100 + number,
                    "floor": floor,
                    "department": rd.choice([
                        "ER","Surgery","Internal Medicine","Pediatrics","Psychiatry",
                        "Oncology","Cardiology","Neurology","Gynecology","Urology"
                    ]),
                    "availability": self.create_schedule()
                })

        # Create maps for quick lookups (adjusted to "number")
        doctor_map = {d["hospital_id"]: d for d in doctors}
        patient_map = {p["hospital_id"]: p for p in patients}
        room_map = {r["number"]: r for r in rooms}

        # Generate appointments
        appointments = []
        for x in range(number_of_appointments):
            doc = rd.choice(doctors)
            pat = rd.choice(patients)
            room = rd.choice(rooms)
            day = rd.choice(self.create_week())
            time = rd.choice(self.create_timeframe())

            appointments.append({
                "appointment_id": x,
                "doctor_hid": doc["hospital_id"],
                "patient_hid": pat["hospital_id"],
                "room_number": room["number"],  # now uses "number"
                "date": day,
                "timeframe": time,
                "status": rd.choice(["Scheduled", "Cancelled"]),
                "diagnosis_id": None,
                "medication_id": None,
            })

            doctor_map[doc["hospital_id"]]["appointments"].append(x)
            patient_map[pat["hospital_id"]]["appointments"].append(x)
            doctor_map[doc["hospital_id"]]["availability"][day][time] = False
            room_map[room["number"]]["availability"][day][time] = False

        # Generate drugs
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

        self.save_to_csv(patients, "./database/patients.csv")
        self.save_to_csv(doctors, "./database/doctors.csv")
        self.save_to_csv(rooms, "./database/rooms.csv")
        self.save_to_csv(appointments, "./database/appointments.csv")
        self.save_to_csv(drugs, "./database/drugs.csv")
