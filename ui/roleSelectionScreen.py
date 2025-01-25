from tkinter import messagebox
import customtkinter as ctk

class RoleSelectionScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Role Selection"
        
        # Empty space
        empty_frame = ctk.CTkFrame(self, fg_color="transparent", height=150)
        empty_frame.pack()
        
        # Title
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(pady=20)
        label = ctk.CTkLabel(title_frame, text="Select Role", font=("Helvetica", 24, "bold"))
        label.grid(row=0, column=2, pady=10)

        # Buttons
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(pady=20)
        ctk.CTkButton(
            buttons_frame, text="Patient",
            command=lambda: self.select_role("patient"),
            width=200, height=50
        ).grid(row=0, column=1, pady=20, padx=20)

        ctk.CTkButton(
            buttons_frame, text="Doctor",
            command=lambda: self.select_role("doctor"),
            width=200, height=50
        ).grid(row=0, column=2, pady=20, padx=20, sticky="ns")

        ctk.CTkButton(
            buttons_frame, text="Administrator",
            command=lambda: self.select_role("admin"),
            width=200, height=50
        ).grid(row=0, column=3, pady=20, padx=20, sticky="ns")

    def select_role(self, role):
        self.controller.selected_role = role
        if role == "patient":
            self.controller.show_frame("LoginScreenPatient")
        elif role == "doctor":
            self.controller.show_frame("LoginScreenDoctor")
        elif role == "admin":
            self.controller.show_frame("LoginScreenAdmin")