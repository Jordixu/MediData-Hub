import pandas as pd
import datetime as dt
import random as rd
from faker import Faker
from typing import Union

class Utilities:
    """
    Utilities class provides various utility functions for handling data processing, 
    file operations, and generating random data for a hospital management system.
    Methods:
        __init__():
            Initializes the Utilities class with a Faker instance for generating fake data.
        load_from_csv(filename: str) -> list:
            Loads data from a CSV file, processes it, and returns a list of dictionaries.
        process_dataframe(df: pd.DataFrame) -> list:
            Processes a DataFrame to convert values to appropriate data types and returns a list of dictionaries.
        process_availability(value: any) -> dict:
            Converts an availability string into a nested dictionary with date and time objects.
        process_date(value: any) -> dt.date:
            Transforms a date string into a date object.
        process_timeframe(value: any) -> tuple:
            Processes a timeframe value and returns it as a tuple of time objects.
        auto_convert(value: any) -> any:
            Converts a value to an appropriate data type (int, float, bool, list of ints, or string).
        save_to_csv(data: list, filename: str) -> None:
            Saves data to a CSV file.
        update_database(hospital) -> None:
            Updates the database with hospital data by saving it to CSV files.
        create_timeframe() -> list:
            Creates a list of timeframes for appointments and returns it.
        create_week() -> list:
            Creates a list of dates for a week and returns it.
        create_schedule() -> dict:
            Creates a schedule for a week with available time slots and returns it.
        random_datas(
            Generates random data for patients, doctors, rooms, appointments, and drugs, and saves them to CSV files.
        validate_and_cast_value(
            value: any, 
            value_type: object, 
            lower: Union[int, float] = None, 
            upper: Union[int, float] = None, 
            custom_message_incorrect_type: str = None, 
            custom_message_lower: str = None, 
            custom_message_upper: str = None
        ) -> object:
            Validates and casts a value to a specified type, optionally checking if it falls within lower and upper bounds.
    """
    
    def __init__(self):
        self.__fake = Faker(['en_US'])

    def load_from_csv(self, filename):
        """
        Loads data from a CSV file, processes it, and returns a list of dictionaries.
        
        Args:
            filename (str): The name of the file to load the data from.
            
        Returns:
            list: A list of dictionaries with the processed data.
        """
        try:
            df = pd.read_csv(filename, sep=';').replace({float('nan'): None}) # Replace NaN values with None
            return self.process_dataframe(df)
        except FileNotFoundError:
            print(f'File {filename} not found.') # Debugging purposes
            return []
        except pd.errors.EmptyDataError:
            print('No data found in the file') # Debugging purposes
            return []

    def process_dataframe(self, df: pd.DataFrame) -> list:
        """
        Processes the data to convert the values in the correct data type (for example, dates, timeframes, etc.).
        
        Args:
            df (DataFrame): The DataFrame to process.
            
        Returns:
            list: A list of dictionaries with the processed data.
        """
        for column in df.columns:
            if column in ['birthday', 'date']:
                df[column] = df[column].apply(self.process_date)
            elif column == 'timeframe':
                df[column] = df[column].apply(self.process_timeframe)
            elif column == 'availability':
                df[column] = df[column].apply(self.process_availability)
            elif column == 'datetime':
                df[column] = pd.to_datetime(df[column], format='%Y-%m-%d %H:%M:%S')
            else:
                df[column] = df[column].apply(self.auto_convert)
        return df.to_dict('records') # 'records' is used to return a list of dictionaries (one for each row)
    
    def process_availability(self, value: any) -> dict:
        """
        Converts the availability string into a nested dictionary with date and time objects.
        """
        if pd.isna(value) or value is None:
            return None
        try:
            namespace = {'datetime': dt}
            availability_dict = eval(value, namespace)
            
            # Process each date and its associated time slots
            processed_dict = {}
            for date_key, time_slots in availability_dict.items():
                date_key = self.process_date(date_key)
                processed_time_slots = {}
                for time_tuple, is_available in time_slots.items():
                    # Check if time_tuple contains datetime.time objects
                    if isinstance(time_tuple[0], dt.time) and isinstance(time_tuple[1], dt.time):
                        processed_time_slots[time_tuple] = is_available
                    else:
                        # Handle string-based time slots (if necessary)
                        try:
                            start_str = str(time_tuple[0])
                            end_str = str(time_tuple[1])
                            start_time = dt.datetime.strptime(start_str, '%H:%M:%S').time()
                            end_time = dt.datetime.strptime(end_str, '%H:%M:%S').time()
                            processed_time_slots[(start_time, end_time)] = is_available
                        except (ValueError, TypeError) as e:
                            print(f"Skipping invalid time slot {time_tuple}: {e}")
                processed_dict[date_key] = processed_time_slots
            return processed_dict
        except Exception as e:
            print(f"Error processing availability: {e}")
            return None

    def process_date(self, value: any) -> dt.date:
        """
        Transform a date string into a date object.
        
        Args:
            value (Any): The value to be transformed.
        
        Returns:
            date: The date object or None if the value is not a valid date.
        """
        # Check if the value is Null, pd.isna is used to check for NaN values (if the conversion failed)
        if pd.isna(value) or value is None:
            return None
        if isinstance(value, dt.date):
            return value
        try:
            # Extract the date part and convert it to a date object, the split is used to remove the time part (just in case it is present, it should not be though)
            return dt.datetime.strptime(value, '%Y-%m-%d').date()
        except (ValueError, AttributeError):
            # Debugging purposes
            print(f"Could not convert value '{value}' to date.")
            return None

    def process_timeframe(self, value: any) -> tuple:
        """
        This method processes a timeframe value and returns it as a tuple of time objects.
        
        Args:
            value (Any): The value to be processed.
        
        Returns:
            tuple: A tuple of time objects or None if the value is not a valid timeframe.
        """
        if pd.isna(value) or value is None: # Check if the value is Null
            return None
        try:
            if ',' in value: # Check if the value may be a tuple of time strings
                timeframe = tuple(value.split(',')) # Convert the string to a tuple
                start_time, end_time = timeframe # Unpack the tuple
                start_time = dt.datetime.strptime(start_time.strip().strip("('").strip("')"), '%H:%M:%S').time() # Convert the time strings to time objects, strip is used to remove the leading/trailing characters
                end_time = dt.datetime.strptime(end_time.strip().strip("('").strip("')"), '%H:%M:%S').time() # Convert the time strings to time objects
                timeframe = (start_time, end_time) # Pack the time objects into a tuple
                return timeframe
            else: 
                return value
        except AttributeError:
            return None

    def auto_convert(self, value: any) -> any:
        """
        Convert a value to an appropriate data type (if it is not a date nor time).

        Args:
            value: The value to be converted.

        Returns:
            The converted value, which can be an int, float, bool, list of ints, or the original string.
        """
        if pd.isnull(value) or value is None: # Check if the value is Null
            return None

        # Try to convert to int, float, bool, or keep as string
        if isinstance(value, str): # Check if it has already been converted
            value = value.strip()  # Remove leading/trailing whitespace
            if value.lower() in ('true', 'false'):  # Handle booleans, case-insensitive
                return value.lower() == 'true'
            try:
                if value.isdigit():  # Check if it's an integer
                    # print("Utilities, l63:", value)
                    return int(value)
                elif '.' in value:  # Check if it's a float
                    return float(value)
                elif '[' in value:  # Check if it's a list of integers
                    inside = value.strip('[]')
                    if ',' in inside:
                        return [int(v.strip()) for v in inside.split(',') if v.strip().isdigit()]
                    else:
                        return [int(inside)] if inside.isdigit() else inside
            except ValueError:
                if any(keyword in value for keyword in ["appointment", "Dr.", "Mr.", "Mrs.", "Ms."]):
                    return
                print(f"Could not convert value '{value}' to int, float, or bool.") # Debugging purposes
        return value # Return the original value if it's not a string (already converted)
    
    def save_to_csv(self, data: list, filename: str) -> None:
        """
        Save data to a CSV file.
        
        Args:
            data (list): The data to save.
            filename (str): The name of the file to save the data to.
        """
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, sep=';', encoding='utf-8')

    def update_database(self, hospital) -> None:
        """
        Updates the database with the hospital data.
        
        Args:
            hospital (Hospital): The hospital object to extract the data from.
        """
        self.save_to_csv(
            [patient.get_all_attributes() for patient in hospital.patients.values()], 
            './database/patients.csv'
            )
        self.save_to_csv(
            [doctor.get_all_attributes() for doctor in hospital.doctors.values()], 
            './database/doctors.csv'
            )
        self.save_to_csv(
            [appointment.get_all_attributes() for appointment in hospital.appointments.values()], 
            './database/appointments.csv'
            )
        self.save_to_csv(
            [room.get_all_attributes() for room in hospital.rooms.values()], 
            './database/rooms.csv'
            )
        self.save_to_csv(
            [notification.get_all_attributes() for notification in hospital.notifications.values()],
            './database/notifications.csv'
            )
        
    def create_timeframe(self):
        """
        Creates a list of timeframes for appointments.
        
        Returns:
            list: A list of tuples with start and end times for each timeframe.
        """
        timeframes = []
        start_time = dt.time(9, 0, 0) # Start time for appointments (9:00 AM)
        end_time = dt.time(21, 0, 0) # End time for appointments (9:00 PM)
        current_time = start_time

        while current_time < end_time: # Create timeframes every hour
            next_time = (dt.datetime.combine(dt.date.today(), current_time) + dt.timedelta(hours=1)).time() # Add one hour to the current time
            timeframes.append((current_time.strftime("%H:%M:%S"), next_time.strftime("%H:%M:%S"))) # Append the current and next time as a tuple
            current_time = next_time # Update the current time
        return timeframes # Return the list of timeframes
        
    def create_week(self):
        """
        Creates a list of dates for a week.
        
        Returns:
            list: A list of date objects for the week.
        """
        week = []
        today = dt.date.today() # Get the current date (to create a week starting from today)
        for i in range(7): # Create a list of dates for the week
            week.append(today + dt.timedelta(days=i)) # Add each day (as string) to the list
        return week
    
    def create_schedule(self):
        """
        Creates a schedule for a week with available time slots.
        
        Returns:
            dict: A dictionary with the schedule for the week.
        """
        schedule = {}
        for day in self.create_week():
            schedule[day] = {}
            for timeframe in self.create_timeframe():
                schedule[day][timeframe] = True
        return schedule

    def random_datas(
        self, 
        number_of_patients: int = 100, 
        number_of_doctors: int = 100, 
        number_of_floors: int = 6, 
        rooms_per_floor: int = 20, 
        number_of_appointments: int = 10000, 
        number_of_drugs: int = 100
    ) -> None:
        # Generate patients
        patients = []
        patient_personal_ids = set() # To avoid duplicates
        for x in range(number_of_patients):
            pid = rd.randint(100000, 999999) # Generate a random personal ID
            if pid not in patient_personal_ids: # Check if the ID is not a duplicate
                patient_personal_ids.add(pid) # Add the ID to the set
                patients.append({
                    "personal_id": pid,
                    "hospital_id": x,
                    "password": self.__fake.password(),
                    "name": self.__fake.name().split()[0],
                    "surname": self.__fake.name().split()[1],
                    "birthday": self.__fake.date_of_birth(minimum_age=16, maximum_age=120),
                    "gender": rd.choice(["Male", "Female"]),
                    "weight": rd.randint(50, 150) + round(rd.uniform(0, 1), 2),
                    "height": rd.randint(150, 200) + round(rd.uniform(0, 1), 2),
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
                "password": self.__fake.password(),
                "name": self.__fake.name().split()[0],
                "surname": self.__fake.name().split()[1],
                "birthday": self.__fake.date_of_birth(minimum_age=25, maximum_age=70),
                "gender": rd.choice(["Male", "Female"]),
                "speciality": rd.choice([
                    "Cardiology", "Dermatology", "Endocrinology", "Gastroenterology", "Hematology", "Infectious Disease", "Nephrology", "Neurology", "Oncology", "Pulmonology", "Rheumatology", "Urology"
                    ]),
                "department": rd.choice([
                    "ER","Surgery","Internal Medicine","Pediatrics","Psychiatry","Oncology",
                    "Cardiology","Neurology","Gynecology","Urology"
                ]),
                "socialsecurity": self.__fake.ssn(taxpayer_identification_number_type="SSN"),
                "salary": rd.randint(40000, 100000) + round(rd.uniform(0, 1), 2),
                "availability": self.create_schedule(),
                "appointments": []
            })

        # Generate rooms
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

        doctorss = {}
        for doctor in doctors:
            doctorss[doctor["hospital_id"]] = doctor
        patientss = {}
        for patient in patients:
            patientss[patient["hospital_id"]] = patient
        roomss = {}
        for room in rooms:
            roomss[room["number"]] = room

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
                "room_number": room["number"],
                "date": day,
                "timeframe": time,
                "status": rd.choices(["Scheduled", "Cancelled"], weights=(0.9, 0.1), k=1)[0],
                "diagnosis_id": None,
                "medication_id": None,
            })

            doctorss[doc["hospital_id"]]["appointments"].append(x)
            patientss[pat["hospital_id"]]["appointments"].append(x)
            doctorss[doc["hospital_id"]]["availability"][day][time] = False
            roomss[room["number"]]["availability"][day][time] = False

        # Generate drugs
        drugs = []
        for x in range(number_of_drugs):
            drugs.append({
                "medication_id": x,
                "name": self.__fake.word(),
                "description": self.__fake.text(max_nb_chars=200),
                "side_effects": self.__fake.text(max_nb_chars=200),
                "dosage": self.__fake.text(max_nb_chars=200),
                "prescription": None,
            })
            
        for doctor in doctors:
            doctor["availability"] = str(doctor["availability"])
        
        for room in rooms:
            room["availability"] = str(room["availability"])

        self.save_to_csv(patients, "./database/patients.csv")
        self.save_to_csv(doctors, "./database/doctors.csv")
        self.save_to_csv(rooms, "./database/rooms.csv")
        self.save_to_csv(appointments, "./database/appointments.csv")
        self.save_to_csv(drugs, "./database/drugs.csv")
        
        
    def validate_and_cast_value(self, value: any,value_type: object, lower: Union[int, float] = None, upper: Union[int, float] = None, custom_message_incorrect_type: str = None, custom_message_lower: str = None, custom_message_upper: str = None) -> object:
        """
        Validates the given value by casting it to a specified type and optionally checking if it falls within lower and upper bounds.
        
        Args:
            value (Any): The value to validate.
            value_type (type): The expected type to cast the value to.
            lower (int | float, optional): The lower bound for the value. Defaults to None.
            upper (int | float, optional): The upper bound for the value. Defaults to None.
            custom_message_incorrect_type (str, optional): A custom error message if the value is not of the expected type. Defaults to None.
            custom_message_lower (str, optional): A custom error message if the value is lower than the lower bound. Defaults to None.
            custom_message_upper (str, optional): A custom error message if the value is greater than the upper bound. Defaults to None.
            
        Raises:
            ValueError: If casting fails or the value falls outside the specified bounds.
            
        Returns:
            Any: The validated (and possibly cast) value.
        """
        try:
            value = value_type(value)
        except ValueError as exc:
            raise ValueError(custom_message_incorrect_type or f"The value must be of type {value_type.__name__}.") from exc
        
        if lower is not None and value < lower:
            raise ValueError(custom_message_lower or f"Value must be greater than {lower}.")
        if upper is not None and value > upper:
            raise ValueError(custom_message_upper or f"Value must be less than {upper}.")

        return value