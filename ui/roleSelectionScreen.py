from tkinter import messagebox
import customtkinter as ctk

class RoleSelectionScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Role Selection"

        # Configure the grid
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)
        for j in range(5):
            self.grid_columnconfigure(j, weight=1)

        # Title
        label = ctk.CTkLabel(self, text="Select Role", font=("Helvetica", 24, "bold"))
        label.grid(row=1, column=2, pady=10)

        # Buttons
        ctk.CTkButton(
            self, text="Patient",
            command=lambda: self.select_role("patient"),
            width=200
        ).grid(row=2, column=1, pady=20, padx=20)

        ctk.CTkButton(
            self, text="Doctor",
            command=lambda: self.select_role("doctor"),
            width=200
        ).grid(row=2, column=2, pady=20, padx=20)

        ctk.CTkButton(
            self, text="Administrator",
            command=self.not_implemented,
            width=200
        ).grid(row=2, column=3, pady=20, padx=20)

    def select_role(self, role):
        self.controller.selected_role = role
        if role == "patient":
            self.controller.show_frame("LoginScreenPatient")
        elif role == "doctor":
            self.controller.show_frame("LoginScreenDoctor")

    def not_implemented(self):
        messagebox.showinfo("Info", "Not implemented yet.")