class Diagnosis():
    def __init__(self, id, title, date, doctor, patient, treatment, description = None):
        self.diagnosis_id = id
        self.title = title
        self.__date = date
        self.__doctor = doctor
        self.__patient = patient
        self.__description = description
        self.__treatment = treatment
        
    def __str__(self):
        return f'{self.__title} on {self.__date} by Dr. {self.__doctor}'