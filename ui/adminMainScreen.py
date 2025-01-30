from tkinter import messagebox
import customtkinter as ctk

class AdminMainScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Admin Main Screen"

        ctk.CTkLabel(self, text="Admin Main Screen", font=("Helvetica", 24)).pack(pady=20)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=10)
        ctk.CTkButton(button_frame, text="Patients", width=200,
            command=lambda: self.not_implemented()).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(button_frame, text="Doctors", width=200,
            command=lambda: self.not_implemented()).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(button_frame, text="Drugs", width=200,
            command=lambda: self.not_implemented()).grid(row=0, column=2, padx=10, pady=10)
        ctk.CTkButton(button_frame, text="Appointments", width=200,
            command=lambda: self.not_implemented()).grid(row=1, column=0, padx=10, pady=10)
        ctk.CTkButton(button_frame, text="Notifications", width=200,
            command=lambda: self.not_implemented()).grid(row=1, column=1, padx=10, pady=10)
        ctk.CTkButton(button_frame, text="Rooms", width=200,
            command=lambda: self.not_implemented()).grid(row=1, column=2, padx=10, pady=10)


        ctk.CTkButton(self, text="Go Back", command=lambda: controller.show_frame("LoginScreenPatient")).pack(pady=20)

    def not_implemented(self):
        messagebox.showinfo("Info", "Not implemented yet.")