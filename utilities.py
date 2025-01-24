import pandas as pd
import datetime as dt

class Data:
    @staticmethod
    def load_from_csv(filename):
        try:
            df = pd.read_csv(filename)
            df = df.where(pd.notnull(df), None)
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
    
    @staticmethod
    def save_to_csv(data, filename):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)

    @staticmethod
    def update_database(hospital):    
        Data.save_to_csv(
            [patient.get_all_attributes() for patient in hospital.patients], 
            './database/patients.csv'
            )
        Data.save_to_csv(
            [doctor.get_all_attributes() for doctor in hospital.doctors], 
            './database/doctors.csv'
            )
        Data.save_to_csv(
            [appointment.get_all_attributes() for appointment in hospital.appointments], 
            './database/appointments.csv'
            )
        Data.save_to_csv(
            [room.get_all_attributes() for room in hospital.rooms], 
            './database/rooms.csv'
            )
        # save_to_csv(drugs_dict, './database/drugs.csv')
        
