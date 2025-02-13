from tkinter import messagebox
import customtkinter as ctk

class PatientMainScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Patient Main Screen"

        ctk.CTkLabel(self, text="Welcome", font=("Helvetica", 24)).pack(pady=20)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20, padx=20, expand=True)

        ctk.CTkButton(button_frame, text="Personal Data", width=220, height=40,
            command=lambda: controller.show_frame("PatientInformation")).grid(row=0, column=0, padx=20, pady=20)
        ctk.CTkButton(button_frame, text="Prescriptions", width=220, height=40,
            command=lambda: controller.show_frame("Prescriptions")).grid(row=0, column=1, padx=20, pady=20)
        ctk.CTkButton(button_frame, text="Appointments", width=220, height=40,
            command=lambda: controller.show_frame("PatientAppointments")).grid(row=1, column=0, padx=20, pady=20)
        ctk.CTkButton(button_frame, text="Notifications", width=220, height=40,
            command=self.not_implemented).grid(row=1, column=1, padx=20, pady=20)

        ctk.CTkButton(self, text="Go Back", width=220, height=40, command=lambda: self.home_button()).pack(pady=20)
        
    def home_button(self):
        self.controller.current_user = None
        self.controller.current_user_data = None
        self.controller.show_frame("RoleSelectionScreen")

    def not_implemented(self):
        messagebox.showinfo("Info", "Not implemented yet.")