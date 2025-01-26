import pandas as pd
import datetime as dt
import numpy as np

# HAY DOS CLASES EN ESTE ARCHIVO

class Data:
    """
    Class to load and save data to CSV files. All methods are static.
    
    Methods:
        load_from_csv(filename): Loads data from a CSV file.
        save_to_csv(data, filename): Saves data to a CSV file.
        update_database(hospital): Updates the database with the hospital data.
    """
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
        
class Datetime:
    """
    Class to create timeframes, weeks, and schedules for the hospital database. All methods are static.
    
    Methods:
        create_timeframe(): Creates a list of timeframes from 9:00 to 21:00 in one-hour intervals.
        create_week(): Creates a list of dates for the current week.
        create_schedule(): Creates a schedule for the current week with timeframes
    """
    @staticmethod
    def create_timeframe():
        timeframes = []
        start_time = dt.time(9, 0)
        end_time = dt.time(21, 0)
        current_time = start_time

        while current_time < end_time:
            next_time = (dt.datetime.combine(dt.date.today(), current_time) + dt.timedelta(hours=1)).time()
            timeframes.append((current_time.strftime("%H:%M"), next_time.strftime("%H:%M")))
            current_time = next_time
        return timeframes
        
    @staticmethod
    def create_week():
        week = []
        today = dt.date.today()
        for i in range(7):
            week.append(today + dt.timedelta(days=i))
        return week
    
    @staticmethod
    def create_schedule():
        schedule = {}
        for day in Datetime.create_week():
            schedule[day] = {}
            for timeframe in Datetime.create_timeframe():
                schedule[day][timeframe] = True
        return schedule
