from tkinter import messagebox
import customtkinter as ctk

class RoleSelectionScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Role Selection"

        # Configure the main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Content area
        
        # Main content area
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        
        # Center the content
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Role selection container
        selection_container = ctk.CTkFrame(content_frame)
        selection_container.place(relx=0.5, rely=0.45, anchor="center")
        
        # Welcome text
        welcome_label = ctk.CTkLabel(
            selection_container, 
            text="Welcome to MediData Hub", 
            font=ctk.CTkFont(size=40, weight="bold")
        )
        welcome_label.pack(pady=(30, 10))
        
        subtitle_label = ctk.CTkLabel(
            selection_container, 
            text="Please select your role to continue", 
            font=ctk.CTkFont(size=20)
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Role buttons container - horizontal layout
        roles_frame = ctk.CTkFrame(selection_container, fg_color="transparent")
        roles_frame.pack(pady=20, padx=40)
        
        # Button styles
        button_width = 220
        button_height = 80
        button_corner_radius = 10
        
        # Patient button
        self.patient_button = ctk.CTkButton(
            roles_frame, 
            text="Patient",
            command=lambda: self.select_role("patient"),
            width=button_width, 
            height=button_height,
            corner_radius=button_corner_radius,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.patient_button.pack(side="left", padx=15)
        
        # Doctor button
        self.doctor_button = ctk.CTkButton(
            roles_frame, 
            text="Doctor",
            command=lambda: self.select_role("doctor"),
            width=button_width, 
            height=button_height,
            corner_radius=button_corner_radius,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.doctor_button.pack(side="left", padx=15)
        
        # Administrator button
        self.admin_button = ctk.CTkButton(
            roles_frame, 
            text="Administrator",
            command=lambda: self.select_role("admin"),
            width=button_width, 
            height=button_height,
            corner_radius=button_corner_radius,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.admin_button.pack(side="left", padx=15)
        
        # Add some padding at the bottom
        bottom_padding = ctk.CTkFrame(selection_container, height=30, fg_color="transparent")
        bottom_padding.pack()

    def select_role(self, role):
        self.controller.selected_role = role
        if role == "patient":
            self.controller.show_frame("LoginScreenPatient")
        elif role == "doctor":
            self.controller.show_frame("LoginScreenDoctor")
        elif role == "admin":
            self.controller.show_frame("LoginScreenAdmin")
            
    def confirm_exit(self):
        if messagebox.askyesno("Exit Application", "Are you sure you want to exit?"):
            self.controller.destroy()