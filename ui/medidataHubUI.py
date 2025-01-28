from ui.roleSelectionScreen import RoleSelectionScreen
from ui.loginScreenPatient import LoginScreenPatient
from ui.registerScreenPatient import RegisterScreenPatient
from ui.loginScreenDoctor import LoginScreenDoctor
from ui.patientMainScreen import PatientMainScreen
from ui.doctorMainScreen import DoctorMainScreen
from ui.patientPrescriptions import Prescriptions
from ui.patientInformation import PatientInformation
from ui.adminAppointments import AdminAppointments
from ui.adminDoctors import AdminDoctors
from ui.adminDrugs import AdminDrugs
from ui.adminMainScreen import AdminMainScreen
from ui.adminNotifications import AdminNotifications
from ui.adminPatients import AdminPatients
from ui.adminRooms import AdminRooms
from ui.loginScreenAdmin import LoginScreenAdmin

from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk

class MedidataHubUI(ctk.CTk):
    def __init__(self, utility, hospital=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Hospital Management System")
        self.selected_role = None
        self.current_user = None
        self.current_user_data = None
        self.utility = utility
        self.hospital = hospital
        self.geometry("800x700")

        menu_container = ctk.CTkFrame(self)
        menu_container.pack(side="top", fill="x")
        
        self.protocol("WM_DELETE_WINDOW", self.quit)
        
        try:
            save_button = ctk.CTkButton(menu_container, text="Save Data", fg_color="#205f25", text_color="white", command=lambda: self.save(), width=30).pack(side="left", padx=10)
            exit_button = ctk.CTkButton(menu_container, text="Exit", command=lambda: self.destroy(), width=30, fg_color="#8B0000").pack(side="right", padx=10)
            exit_and_save_button = ctk.CTkButton(menu_container, text="Exit and Save Data", fg_color="#955600", text_color="white", command=lambda: [self.save(), self.destroy()], width=30).pack(side="right", padx=10)
        except:
            pass

        container = ctk.CTkFrame(self)
        container.pack(side="bottom", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("ui/theme.json")
        
        self.frames = {}
        for F in (
            RoleSelectionScreen, LoginScreenPatient, RegisterScreenPatient, LoginScreenDoctor, PatientMainScreen,DoctorMainScreen, Prescriptions, PatientInformation, AdminAppointments, AdminDoctors, AdminDrugs, AdminMainScreen, AdminNotifications, AdminPatients, AdminRooms, LoginScreenAdmin
        ):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("RoleSelectionScreen")
        
    def save(self):
        self.utility.update_database(self.hospital)
        messagebox.showinfo("Info", "Data saved successfully.")
    
    def quit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit? Make sure you saved all the important data", icon="warning", default="no"):
            self.destroy()

    def show_frame(self, name):
        frame = self.frames[name]
        self.title(frame.title)
        frame.tkraise()