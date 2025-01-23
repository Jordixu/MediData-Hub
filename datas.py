import pandas as pd
import datetime as dt

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def load_from_csv(filename):
    df = pd.read_csv(filename)
    return df

def update_database(hospital):    
    save_to_csv(
        [patient.get_all_attributes() for patient in hospital.patients], 
        './database/patients.csv'
        )
    save_to_csv(
        [doctor.get_all_attributes() for doctor in hospital.doctors], 
        './database/doctors.csv'
        )
    save_to_csv(
        [appointment.get_all_attributes() for appointment in hospital.appointments], 
        './database/appointments.csv')
    save_to_csv(
        [room.get_all_attributes() for room in hospital.rooms], 
        './database/rooms.csv')
    # save_to_csv(drugs_dict, './database/drugs.csv')