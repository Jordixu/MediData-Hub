from tkinter import messagebox
import customtkinter as ctk

class DoctorMainScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Doctor Main Screen"
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        
        header_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 30), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(header_frame, text="Doctor Dashboard", 
                    font=ctk.CTkFont(family="Helvetica", size=42, weight="bold"),
                    text_color="#262850").pack(pady=15)
        
        menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        menu_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        menu_frame.grid_columnconfigure((0, 1), weight=1, uniform="column")
        menu_frame.grid_rowconfigure((0, 1), weight=1, uniform="row")
        
        button_font = ctk.CTkFont(size=22, weight="bold")
        button_height = 80
        
        self.create_button(menu_frame, "Personal Data", "DoctorInformation", 0, 0, button_font, button_height)
        self.create_button(menu_frame, "Consultations", "DoctorConsultation", 0, 1, button_font, button_height)
        self.create_button(menu_frame, "Notifications", "DoctorNotifications", 1, 0, button_font, button_height)
        self.create_button(menu_frame, "Appointments", "DoctorAppointments", 1, 1, button_font, button_height)
        
        sign_out_frame = ctk.CTkFrame(self, fg_color="transparent")
        sign_out_frame.grid(row=2, column=0, pady=(20, 30))
        
        sign_out_button = ctk.CTkButton(
            self,
            text="Sign Out",
            command=self.home_button,
            width=180,
            height=40,
            font=ctk.CTkFont(size=16),
            fg_color="#c0392b",
            hover_color="#e74c3c"
        )
        sign_out_button.place(relx=0.5, rely=0.85, anchor="center")

    def create_button(self, parent, text, target_frame, row, column, font, height):
        button = ctk.CTkButton(
            parent,
            text=text,
            command=lambda tf=target_frame: self.controller.show_frame(tf),
            font=font,
            height=height,
            corner_radius=10
        )
        button.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        return button

    def home_button(self):
        self.controller.current_user = None
        self.controller.current_user_data = None
        self.controller.show_frame("RoleSelectionScreen")