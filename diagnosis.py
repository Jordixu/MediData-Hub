class Diagnosis():
    def __init__(self, id, title, date, doctor, patient, description, treatment):
        self.id = id
        self.title = title
        self.date = date
        self.doctor = doctor
        self.patient = patient
        self.description = description
        self.treatment = treatment
        
    def __str__(self):
        return f'{self.title} on {self.date} by Dr. {self.doctor}'