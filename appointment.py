class Appointment():
    def __init__(self, date, time, doctor, patient, room):
        self.date = date # string
        self.time = time # tuple
        self.doctor = doctor # Doctor
        self.patient = patient # Patient
        self.room = room # Space

    def __str__(self):
        return f'{self.date} at {self.time} with Dr. {self.doctor}'
    
    def change_date(self, date):
        self.date = date
    
    def change_time(self, time):
        self.time = time
    
    def change_doctor(self, doctor):
        self.doctor = doctor
    
    def change_patient(self, patient):
        self.patient = patient
    
    def change_room(self, room):
        self.room = room