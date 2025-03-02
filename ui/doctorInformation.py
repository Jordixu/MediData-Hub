from tkinter import messagebox
import tkinter as tk
import datetime as dt
import customtkinter as ctk
from tkinter import ttk

class DoctorInformation(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Doctor Information"
        
        # Configure the main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Title
        self.grid_rowconfigure(1, weight=1)  # Form content
        self.grid_rowconfigure(2, weight=0)  # Buttons
        
        # Title
        title_label = ctk.CTkLabel(
            self, 
            text="Doctor Information", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(30, 20))
        
        # Main content container
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, padx=20, sticky="n")
        
        # Configure columns for the two sections
        content_frame.grid_columnconfigure(0, weight=1)  # Left section
        content_frame.grid_columnconfigure(1, weight=0)  # Divider
        content_frame.grid_columnconfigure(2, weight=1)  # Right section
        
        # Left section - Account Information
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, padx=20, pady=10, sticky="n")
        
        ctk.CTkLabel(
            left_frame, 
            text="Account Information", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(0, 15))
        
        # Name field
        ctk.CTkLabel(left_frame, text="Name", anchor="w").pack(anchor="w", pady=(5, 2))
        self.name_label = ctk.CTkLabel(
            left_frame,
            text="",
            anchor="w",
            height=30,
            fg_color="#F0F0F0",
            corner_radius=6
        )
        self.name_label.pack(pady=(0, 10), fill="x")
        
        # Surname field
        ctk.CTkLabel(left_frame, text="Surname", anchor="w").pack(anchor="w", pady=(5, 2))
        self.surname_label = ctk.CTkLabel(
            left_frame,
            text="",
            anchor="w",
            height=30,
            fg_color="#F0F0F0",
            corner_radius=6
        )
        self.surname_label.pack(pady=(0, 10), fill="x")
        
        # Social Security Number field
        ctk.CTkLabel(left_frame, text="Social Security Number", anchor="w").pack(anchor="w", pady=(5, 2))
        self.ssn_label = ctk.CTkLabel(
            left_frame,
            text="",
            anchor="w",
            height=30,
            fg_color="#F0F0F0",
            corner_radius=6
        )
        self.ssn_label.pack(pady=(0, 10), fill="x")
        
        # Gender selection
        ctk.CTkLabel(left_frame, text="Gender", anchor="w").pack(anchor="w", pady=(5, 2))
        gender_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        gender_frame.pack(pady=(0, 10), fill="x")
        
        self.gender_var = tk.StringVar(value="")
        male_radio = ctk.CTkRadioButton(
            gender_frame, 
            text="Male", 
            variable=self.gender_var, 
            value="Male",
            state="disabled"
        )
        male_radio.pack(side="left", padx=(0, 20))
        
        female_radio = ctk.CTkRadioButton(
            gender_frame, 
            text="Female", 
            variable=self.gender_var, 
            value="Female",
            state="disabled"
        )
        female_radio.pack(side="left")
        
        # Birthday field
        ctk.CTkLabel(left_frame, text="Birthday", anchor="w").pack(anchor="w", pady=(5, 2))
        self.birthday_label = ctk.CTkLabel(
            left_frame,
            text="",
            anchor="w",
            height=30,
            fg_color="#F0F0F0",
            corner_radius=6
        )
        self.birthday_label.pack(pady=(0, 10), fill="x")
        
        # Vertical line separator
        separator = ctk.CTkFrame(content_frame, width=1, fg_color="gray80")
        separator.grid(row=0, column=1, sticky="ns", padx=10, pady=10)
        
        # Right section - Professional Information
        right_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_frame.grid(row=0, column=2, padx=20, pady=10, sticky="n")
        
        ctk.CTkLabel(
            right_frame, 
            text="Professional Information", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(0, 15))
        
        # Personal ID field
        ctk.CTkLabel(right_frame, text="Personal ID", anchor="w").pack(anchor="w", pady=(5, 2))
        self.personal_id_label = ctk.CTkLabel(
            right_frame,
            text="",
            anchor="w",
            height=30,
            fg_color="#F0F0F0",
            corner_radius=6
        )
        self.personal_id_label.pack(pady=(0, 10), fill="x")
        
        # Hospital ID field
        ctk.CTkLabel(right_frame, text="Hospital ID", anchor="w").pack(anchor="w", pady=(5, 2))
        self.hospital_id_label = ctk.CTkLabel(
            right_frame,
            text="",
            anchor="w",
            height=30,
            fg_color="#F0F0F0",
            corner_radius=6
        )
        self.hospital_id_label.pack(pady=(0, 10), fill="x")
        
        # Department field
        ctk.CTkLabel(right_frame, text="Department", anchor="w").pack(anchor="w", pady=(5, 2))
        self.department_label = ctk.CTkLabel(
            right_frame,
            text="",
            anchor="w",
            height=30,
            fg_color="#F0F0F0",
            corner_radius=6
        )
        self.department_label.pack(pady=(0, 10), fill="x")
        
        # Specialty field
        ctk.CTkLabel(right_frame, text="Specialty", anchor="w").pack(anchor="w", pady=(5, 2))
        self.specialty_label = ctk.CTkLabel(
            right_frame,
            text="",
            anchor="w",
            height=30,
            fg_color="#F0F0F0",
            corner_radius=6
        )
        self.specialty_label.pack(pady=(0, 10), fill="x")
        
        # Change Password button
        change_pass_btn = ctk.CTkButton(
            right_frame, 
            text="Change Password",
            width=200,
            height=35,
            fg_color="#003366",
            hover_color="#004080",
            command=lambda: controller.show_frame("ChangePassword")
        )
        change_pass_btn.pack(pady=(15, 5))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.grid(row=2, column=0, pady=(20, 30))
        
        # Go Back button
        back_btn = ctk.CTkButton(
            buttons_frame, 
            text="Go Back", 
            command=lambda: controller.show_frame("DoctorMainScreen"),
            width=150,
            height=35,
            fg_color="#555555",
            hover_color="#666666"
        )
        back_btn.pack(side="left", padx=5)

    def load_data(self):
        try:
            # Load Name
            name = self.controller.current_user_data.get_protected_attribute("name")
            self.name_label.configure(text=name)
            
            # Load Surname
            surname = self.controller.current_user_data.get_protected_attribute("surname")
            self.surname_label.configure(text=surname)
            
            # Load SSN
            ssn = self.controller.current_user_data.get("socialsecurity")
            self.ssn_label.configure(text=ssn)
            
            # Set Gender
            self.gender_var.set(self.controller.current_user_data.get_protected_attribute("gender"))
            
            # Set Birthday
            birthday_str = self.controller.current_user_data.get_protected_attribute("birthday")
            if isinstance(birthday_str, str):
                birthday_date = dt.datetime.strptime(birthday_str, "%Y-%m-%d").date()
                formatted_birthday = birthday_date.strftime("%d/%m/%Y")
            elif isinstance(birthday_str, dt.date):
                formatted_birthday = birthday_str.strftime("%d/%m/%Y")
            else:
                formatted_birthday = "Not specified"
                
            self.birthday_label.configure(text=formatted_birthday)
            
            # Load Personal ID
            personal_id = self.controller.current_user_data.get_protected_attribute("personal_id")
            self.personal_id_label.configure(text=personal_id)
            
            # Load Hospital ID
            hospital_id = self.controller.current_user_data.get_protected_attribute("hospital_id")
            self.hospital_id_label.configure(text=hospital_id)
            
            # Load Department
            department = self.controller.current_user_data.get("department", "Not assigned")
            self.department_label.configure(text=department)
            
            # Load Specialty
            specialty = self.controller.current_user_data.get("speciality", "Not specified")
            self.specialty_label.configure(text=specialty)

        except AttributeError as exc:
            messagebox.showerror("Error", str(exc))
            
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_data()