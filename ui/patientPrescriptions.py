from tkinter import messagebox
import customtkinter as ctk

class Prescriptions(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Prescriptions"

        ctk.CTkLabel(self, text="Patient: Prescriptions", font=("Helvetica", 16)).pack(pady=10)

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(pady=10)

        headers = ["Name", "Dosage", "Duration", "By Doctor (name)"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(table_frame, text=header, font=("Helvetica", 10, "bold"), width=100).grid(row=0, column=i, padx=1, pady=1)

        for row in range(1, 6):
            for col in range(len(headers)):
                ctk.CTkLabel(table_frame, text="", width=100).grid(row=row, column=col, padx=1, pady=1)

        ctk.CTkButton(self, text="Go Back", command=lambda: controller.show_frame("PatientMainScreen")).pack(side="left", pady=20, padx=20)
        ctk.CTkButton(self, text="More", command=self.not_implemented).pack(side="right", pady=20, padx=20)

    def not_implemented(self):
        messagebox.showinfo("Info", "Not implemented yet.")