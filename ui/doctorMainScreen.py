from tkinter import messagebox
import customtkinter as ctk

class DoctorMainScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Doctor Main Screen"

        ctk.CTkLabel(self, text="Doctor Main Screen", font=("Helvetica", 16)).pack(pady=10)

        ctk.CTkButton(self, text="Prescriptions", command=self.not_implemented).pack(pady=5)
        ctk.CTkButton(self, text="Appointments", command=self.not_implemented).pack(pady=5)
        ctk.CTkButton(self, text="Notifications", command=self.not_implemented).pack(pady=5)
        ctk.CTkButton(self, text="Go Back", command=lambda: controller.show_frame("RoleSelectionScreen")).pack(pady=10)

    def not_implemented(self):
        messagebox.showinfo("Info", "Not implemented yet.")