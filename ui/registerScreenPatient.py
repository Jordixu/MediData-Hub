from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from tkcalendar import DateEntry
from datetime import date

class RegisterScreenPatient(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Register"
        
        # Configure the main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Title
        self.grid_rowconfigure(1, weight=1)  # Form content
        self.grid_rowconfigure(2, weight=0)  # Buttons
        
        # Title
        title_label = ctk.CTkLabel(
            self, 
            text="Patient Registration", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(30, 20))
        
        # Main content container - uses grid for a clean layout
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, padx=20, sticky="n")
        
        # Configure columns for the two sections
        content_frame.grid_columnconfigure(0, weight=1)  # Left section
        content_frame.grid_columnconfigure(1, weight=0)  # Divider
        content_frame.grid_columnconfigure(2, weight=1)  # Right section
        
        # Left section - Login Information
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, padx=20, pady=10, sticky="n")
        
        ctk.CTkLabel(
            left_frame, 
            text="Login Information", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(0, 15))
        
        # Personal ID field
        ctk.CTkLabel(left_frame, text="Personal ID (User)", anchor="w").pack(anchor="w", pady=(5, 2))
        self.user_entry = ctk.CTkEntry(
            left_frame, 
            placeholder_text="Enter your ID number", 
            width=250, 
            height=30
        )
        self.user_entry.pack(pady=(0, 10), fill="x")
        
        # Password field
        ctk.CTkLabel(left_frame, text="Password", anchor="w").pack(anchor="w", pady=(5, 2))
        self.pass_entry = ctk.CTkEntry(
            left_frame, 
            placeholder_text="Create a password", 
            show='•', 
            width=250, 
            height=30
        )
        self.pass_entry.pack(pady=(0, 10), fill="x")
        
        # Confirm password field
        ctk.CTkLabel(left_frame, text="Confirm Password", anchor="w").pack(anchor="w", pady=(5, 2))
        self.confirm_pass_entry = ctk.CTkEntry(
            left_frame, 
            placeholder_text="Confirm your password", 
            show='•', 
            width=250, 
            height=30
        )
        self.confirm_pass_entry.pack(pady=(0, 10), fill="x")
        
        # Vertical line separator
        separator = ctk.CTkFrame(content_frame, width=1, fg_color="gray80")
        separator.grid(row=0, column=1, sticky="ns", padx=10, pady=10)
        
        # Right section - Personal Information
        right_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_frame.grid(row=0, column=2, padx=20, pady=10, sticky="n")
        
        ctk.CTkLabel(
            right_frame, 
            text="Personal Information", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(0, 15))
        
        # Name field
        ctk.CTkLabel(right_frame, text="Name", anchor="w").pack(anchor="w", pady=(5, 2))
        self.name_entry = ctk.CTkEntry(
            right_frame, 
            placeholder_text="Enter your name", 
            width=250, 
            height=30
        )
        self.name_entry.pack(pady=(0, 10), fill="x")
        
        # Surname field
        ctk.CTkLabel(right_frame, text="Surname", anchor="w").pack(anchor="w", pady=(5, 2))
        self.surname_entry = ctk.CTkEntry(
            right_frame, 
            placeholder_text="Enter your surname", 
            width=250, 
            height=30
        )
        self.surname_entry.pack(pady=(0, 10), fill="x")
        
        # Gender selection
        ctk.CTkLabel(right_frame, text="Gender", anchor="w").pack(anchor="w", pady=(5, 2))
        gender_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        gender_frame.pack(pady=(0, 10), fill="x")
        
        self.gender_var = tk.StringVar(value="")
        male_radio = ctk.CTkRadioButton(
            gender_frame, 
            text="Male", 
            variable=self.gender_var, 
            value="Male"
        )
        male_radio.pack(side="left", padx=(0, 20))
        
        female_radio = ctk.CTkRadioButton(
            gender_frame, 
            text="Female", 
            variable=self.gender_var, 
            value="Female"
        )
        female_radio.pack(side="left")
        
        # Birthday field
        ctk.CTkLabel(right_frame, text="Birthday", anchor="w").pack(anchor="w", pady=(5, 2))
        
        date_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        date_frame.pack(pady=(0, 10), fill="x")
        
        self.birthday_entry = DateEntry(
            date_frame, 
            width=12, 
            background='white', 
            foreground='black', 
            borderwidth=1, 
            font=('Helvetica', 12), 
            date_pattern='dd/MM/yyyy',
            maxdate=date.today()
        )
        self.birthday_entry.pack(fill="x", ipady=3)
        
        # Weight field
        ctk.CTkLabel(right_frame, text="Weight (kg)", anchor="w").pack(anchor="w", pady=(5, 2))
        self.weight_entry = ctk.CTkEntry(
            right_frame, 
            placeholder_text="Enter your weight", 
            width=250, 
            height=30
        )
        self.weight_entry.pack(pady=(0, 10), fill="x")
        
        # Height field
        ctk.CTkLabel(right_frame, text="Height (cm)", anchor="w").pack(anchor="w", pady=(5, 2))
        self.height_entry = ctk.CTkEntry(
            right_frame, 
            placeholder_text="Enter your height", 
            width=250, 
            height=30
        )
        self.height_entry.pack(pady=(0, 10), fill="x")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.grid(row=2, column=0, pady=(20, 30))
        
        # Submit button
        submit_btn = ctk.CTkButton(
            buttons_frame, 
            text="Submit", 
            command=self.submit_data,
            width=150,
            height=35,
            fg_color="#003366",
            hover_color="#004080"
        )
        submit_btn.pack(side="left", padx=5)
        
        # Go Back button
        back_btn = ctk.CTkButton(
            buttons_frame, 
            text="Go Back", 
            command=lambda: controller.show_frame("LoginScreenPatient"),
            width=150,
            height=35,
            fg_color="#555555",
            hover_color="#666666"
        )
        back_btn.pack(side="left", padx=5)

    def clear_entries(self):
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)
        self.confirm_pass_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.surname_entry.delete(0, tk.END)
        self.gender_var.set("")
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)

    def submit_data(self):
        personal_id = self.user_entry.get()
        password = self.pass_entry.get()
        confirm_password = self.confirm_pass_entry.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        gender = self.gender_var.get()
        birthday = self.birthday_entry.get_date()
        weight = self.weight_entry.get()
        height = self.height_entry.get()

        # Check if passwords match
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        fields = [name, surname, gender, birthday, weight, height, personal_id, password]
        if all(fields):
            if name.isalpha() and surname.isalpha():
                try:
                    self.controller.hospital.add_patient(
                        personal_id=personal_id,
                        password=password,
                        name=name,
                        surname=surname,
                        birthday=birthday,
                        gender=gender,
                        weight=weight,
                        height=height
                    )
                    messagebox.showinfo("Success", "Registration completed successfully!")
                    self.clear_entries()
                    self.controller.show_frame("LoginScreenPatient")
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showerror("Error", "Name and surname must contain only letters")
        else:
            messagebox.showerror("Error", "Please fill out all fields")