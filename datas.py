import pandas as pd
from hospital import Hospital
import datetime as dt

"""
This file is used to save the data from the hospital object to csv files.
We are not really
"""

def patients_list_to_dict(patients):
    patients_list = []
    for patient in patients:
        patients_list.append({
            'Id': patient.id,
            'Name': patient.name,
            'Surname': patient.surname,
            'Age': patient.age,
            'Gender': patient.sex,
            'Weight': patient.weight,
            'Height': patient.height,
            'Assigned_doctor': patient.assigned_doctor,
            'Status': patient.status,
            'Appointments': patient.appointments,
            'Medications': patient.medications,
            'Allergies': patient.allergies,
            'Diagnostics': patient.diagnostics
        })
    return patients_list

def doctors_list_to_dict(doctors):
    doctors_list = []
    for doctor in doctors:
        doctors_list.append({
            'Id': doctor.id,
            'Name': doctor.name,
            'Surname': doctor.surname,
            'Age': doctor.age,
            'Gender': doctor.gender,
            'Speciality': doctor.speciality,
            'Department': doctor.department,
            'Availability': doctor.availability,
            'Socialsecurity': doctor.socialsecurity,
            'Salary': doctor.salary,
            'Assigned_patients': doctor.assigned_patients
        })
    return doctors_list

def appointments_to_dict(appointments):
    appointments_list = []
    for appointment in appointments:
        appointments_list.append({
            'Date': appointment.date,
            'Time': appointment.time,
            'Doctor': appointment.doctor.name,
            'Patient': appointment.patient.name, 
            'Room': appointment.room.number,
            'Status': appointment.status
        })
    return appointments_list

def rooms_to_dict(rooms):
    rooms_list = []
    for room in rooms:
        rooms_list.append({
            'Number': room.number,
            'Floor': room.floor,
            'Department': room.department,
            'Availability': room.availability
        })
    return rooms_list

def drugs_to_dict(drugs):
    drugs_list = []
    for drug in drugs:
        drugs_list.append({
            'Id': drug.id,
            'Name': drug.name,
            'Description': drug.description
        })
    return drugs_list

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def load_from_csv(filename):
    df = pd.read_csv(filename)
    return df

def update_database():
    patients_dict = patients_list_to_dict(Hospital.patients)
    doctors_dict = doctors_list_to_dict(Hospital.doctors)
    appointments_dict = appointments_to_dict(Hospital.appointments)
    rooms_dict = rooms_to_dict(Hospital.rooms)
    drugs_dict = drugs_to_dict(Hospital.drugs)
    
    save_to_csv(patients_dict, './database/patients.csv')
    save_to_csv(doctors_dict, './database/doctors.csv')
    save_to_csv(appointments_dict, './database/appointments.csv')
    save_to_csv(rooms_dict, './database/rooms.csv')
    save_to_csv(drugs_dict, './database/drugs.csv')

update_database()