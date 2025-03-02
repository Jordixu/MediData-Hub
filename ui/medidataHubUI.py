from ui.roleSelectionScreen import RoleSelectionScreen
from ui.loginScreenPatient import LoginScreenPatient
from ui.registerScreenPatient import RegisterScreenPatient
from ui.loginScreenDoctor import LoginScreenDoctor
from ui.patientMainScreen import PatientMainScreen
from ui.doctorMainScreen import DoctorMainScreen
from ui.patientPrescriptions import PatientPrescriptions
from ui.patientInformation import PatientInformation
from ui.adminMainScreen import AdminMainScreen
from ui.loginScreenAdmin import LoginScreenAdmin
from ui.patientAppointments import PatientAppointments
from ui.ChangePassword import ChangePassword
from ui.patientRequestAppointment import PatientRequestAppointment
from ui.doctorNotifications import DoctorNotifications
from ui.doctorNotificationsDetailsRequest import DoctorNotificationsDetailsRequest
from ui.notificationsDetails import NotificationsDetails
from ui.doctorInformation import DoctorInformation
from ui.doctorAppointments import DoctorAppointments
from ui.patientNotifications import PatientNotifications
from ui.doctorConsultation import DoctorConsultation
from ui.adminAppointments import AdminAppointments
from ui.adminDoctors import AdminDoctors
from ui.adminPatients import AdminPatients
from ui.adminRooms import AdminRooms
from ui.adminDrugs import AdminDrugs
from ui.adminNotifications import AdminNotifications
from ui.adminViewAppointmentsRoom import AdminViewAppointmentsRoom
from ui.adminAddDoctor import AdminAddDoctor
from ui.adminAddDrugs import AdminAddDrugs
from ui.doctorConsultationCreate import DoctorConsultationCreate
from ui.adminModifyDoctor import AdminModifyDoctor
from ui.adminModifyDrugs import AdminModifyDrugs
from ui.appointmentDetails import AppointmentDetails

from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk

class MedidataHubUI(ctk.CTk):
    def __init__(self, utility, hospital=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Hospital Management System")
        self.resizable(False, False)
        
        # Set window to use almost full screen size
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Use about 90% of screen size
        width = int(screen_width * 0.9)
        height = int(screen_height * 0.8)
        
        # Center the window
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2 - 50
        
        # Set geometry with position and size
        self.geometry(f"{width}x{height}+{x}+{y}")        
        
        self.selected_role = None
        self.current_user = None # The id of the current user
        self.current_user_data = None # The data of the current user
        self.utility = utility
        self.hospital = hospital
        self.selected_notification = None
        self.selected_appointment = None
        self.selected_doctor = None
        self.selected_patient = None
        self.selected_room = None
        self.selected_drug = None
        
        self.protocol("WM_DELETE_WINDOW", self.quit)
        
        self.create_top_menu()

        container = ctk.CTkFrame(self, fg_color="#ffffff")
        container.pack(side="bottom", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("ui/theme.json")
        
        self.frames = {}
        for F in (
            RoleSelectionScreen, LoginScreenPatient, RegisterScreenPatient, LoginScreenDoctor, PatientMainScreen,DoctorMainScreen, PatientPrescriptions, PatientInformation, AdminMainScreen, LoginScreenAdmin, PatientAppointments, ChangePassword, PatientRequestAppointment, DoctorNotifications, DoctorNotificationsDetailsRequest, NotificationsDetails, DoctorInformation, DoctorAppointments, PatientNotifications, DoctorConsultation, AdminAppointments, AdminDoctors, AdminPatients, AdminRooms, AdminDrugs, AdminNotifications, AdminViewAppointmentsRoom, AdminAddDoctor, AdminAddDrugs, DoctorConsultationCreate, AdminModifyDoctor, AdminModifyDrugs, AppointmentDetails
        ):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("RoleSelectionScreen")
    
    def create_top_menu(self):
        
        menu_container = ctk.CTkFrame(self, corner_radius=0, fg_color="#f0f5fa", height=60)
        menu_container.pack(side="top", fill="x")
        menu_container.pack_propagate(False)
        
        left_frame = ctk.CTkFrame(menu_container, fg_color="transparent")
        left_frame.pack(side="left", fill="y")
        
        app_label = ctk.CTkLabel(
            left_frame, 
            text="MediData Hub", 
            font=("Helvetica", 18, "bold"),
            text_color="#2D5A88"
        )
        app_label.pack(side="left", padx=20, pady=10)
        
        # Add a separator
        separator = ctk.CTkFrame(menu_container, width=1, fg_color="#d1d5db")
        separator.pack(side="left", fill="y", padx=5, pady=10)
        
        self.center_frame = ctk.CTkFrame(menu_container, fg_color="transparent")
        self.center_frame.pack(side="left", fill="y", expand=True)
        
        # Right side - Action buttons
        right_frame = ctk.CTkFrame(menu_container, fg_color="transparent")
        right_frame.pack(side="right", fill="y")
        
        # Save button
        save_button = ctk.CTkButton(
            right_frame,
            text="Save Data",
            width=110,
            height=30,
            corner_radius=8,
            fg_color="#3182CE",
            text_color="white",
            hover_color="#2C5282",
            command=self.save
        )
        save_button.pack(side="left", padx=5, pady=10)
        
        # Save and exit button
        save_exit_button = ctk.CTkButton(
            right_frame,
            text="Save & Exit",
            width=110,
            height=30,
            corner_radius=8,
            fg_color="#ED8936",
            text_color="white",
            hover_color="#C05621",
            command=lambda: [self.save(), self.destroy()]
        )
        save_exit_button.pack(side="left", padx=5, pady=10)
        
        # Exit button
        exit_button = ctk.CTkButton(
            right_frame,
            text="Exit",
            width=80,
            height=30,
            corner_radius=8,
            fg_color="#E53E3E",
            text_color="white",
            hover_color="#C53030",
            command=self.quit
        )
        exit_button.pack(side="left", padx=(5, 20), pady=10)
        
        bottom_border = ctk.CTkFrame(self, height=1, fg_color="#d1d5db")
        bottom_border.pack(side="top", fill="x")
        
    def save(self):
        self.utility.update_database(self.hospital)
        messagebox.showinfo("Info", "Data saved successfully.")

    def quit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit? Make sure you saved all the important data", icon="warning", default="no"):
            self.destroy()
            
    def refresh_selected_data(self):
        self.selected_appointment = None
        self.selected_notification = None
        self.selected_doctor = None
        self.selected_patient = None
        self.selected_room = None
        self.selected_drug = None

    def refresh_user_data(self):
        self.current_user_data = None
        self.current_user = None

    def show_frame(self, name):
        frame = self.frames[name]
        self.title(frame.title)
        frame.tkraise()