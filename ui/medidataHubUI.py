from ui.roleSelectionScreen import RoleSelectionScreen
from ui.loginScreenPatient import LoginScreenPatient
from ui.registerScreenPatient import RegisterScreenPatient
from ui.loginScreenDoctor import LoginScreenDoctor
from ui.patientMainScreen import PatientMainScreen
from ui.doctorMainScreen import DoctorMainScreen
from ui.prescriptions import Prescriptions
from ui.patientInformation import PatientInformation

from tkinter import messagebox
import customtkinter as ctk

class MedidataHubUI(ctk.CTk):
    def __init__(self, hospital=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Hospital Management System")
        self.selected_role = None
        self.current_user = None
        self.current_user_data = None
        self.hospital = hospital
        self.geometry("800x600")

        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("ui/theme.json")
        
        self.frames = {}
        for F in (
            RoleSelectionScreen, LoginScreenPatient, RegisterScreenPatient, LoginScreenDoctor, PatientMainScreen,DoctorMainScreen, Prescriptions, PatientInformation
        ):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("RoleSelectionScreen")

    def show_frame(self, name):
        frame = self.frames[name]
        self.title(frame.title)
        frame.tkraise()