class Appointment():
    def __init__(self, date, timeframe, doctor, patient, room, status):
        """
        Initializes a new appointment.
        Args:
            date (date or str): The date of the appointment.
            timeframe (tuple): The timeframe or time slot for the appointment.
            doctor (str or object): The doctor assigned to the appointment.
            patient (str or object): The patient who has the appointment.
            room (str): The location or room where the appointment will take place.
            status (str): The current status of the appointment (e.g., 'scheduled', 'completed').
        Attributes:
            date (date or str): The date of the appointment.
            time (str): The timeframe or time slot for the appointment.
            doctor (str or object): The assigned doctor for the appointment.
            patient (str or object): The patient who has the appointment.
            room (str): The designated location or room for the appointment.
            status (str): The current status of the appointment in its lifecycle.
        """  
        self.date = date
        self.time = timeframe
        self.doctor = doctor
        self.patient = patient
        self.room = room
        self.status = status

    def __str__(self):
        return f'{self.date} at {self.timeframe} with Dr. {self.doctor}'
    
    def change_date(self, date):
        self.date = date
    
    def change_time(self, timeframe):
        if type(timeframe) != tuple:
            return 'The timeframe must be a tuple'
        self.timeframe = timeframe
    
    def change_doctor(self, doctor):
        self.doctor = doctor
    
    def change_patient(self, patient):
        self.patient = patient
    
    def change_room(self, room):
        self.room = room