from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from tkcalendar import DateEntry
from datetime import date
import re

class AdminModifyDoctor(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Modify Doctor"
        
        # Data for specialty and department dropdowns
        self.specialties = ["Cardiology", "Dermatology", "Endocrinology", "Gastroenterology", 
                   "Hematology", "Infectious Disease", "Nephrology", "Neurology", 
                   "Oncology", "Pulmonology", "Rheumatology", "Urology"]
        self.departments = ["ER", "Surgery", "Internal Medicine", "Pediatrics", "Psychiatry", 
                   "Oncology", "Cardiology", "Neurology", "Gynecology", "Urology"]
        
        # Configure the main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Title
        self.grid_rowconfigure(1, weight=1)  # Form content
        self.grid_rowconfigure(2, weight=0)  # Buttons
        
        # Title
        title_label = ctk.CTkLabel(
            self, 
            text="Modify Doctor", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(30, 20))
        
        # Main container
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
        
        # Personal ID field (read-only)
        ctk.CTkLabel(left_frame, text="Personal ID (User)", anchor="w").pack(anchor="w", pady=(5, 2))
        self.user_entry = ctk.CTkEntry(
            left_frame, 
            placeholder_text="Enter ID number", 
            width=250, 
            height=30,
            state="disabled"  # Make it read-only
        )
        self.user_entry.pack(pady=(0, 10), fill="x")
        
        # Password field
        ctk.CTkLabel(left_frame, text="New Password (optional)", anchor="w").pack(anchor="w", pady=(5, 2))
        self.pass_entry = ctk.CTkEntry(
            left_frame, 
            placeholder_text="Leave blank to keep current", 
            show='•', 
            width=250, 
            height=30
        )
        self.pass_entry.pack(pady=(0, 10), fill="x")
        
        # Confirm password field
        ctk.CTkLabel(left_frame, text="Confirm New Password", anchor="w").pack(anchor="w", pady=(5, 2))
        self.confirm_pass_entry = ctk.CTkEntry(
            left_frame, 
            placeholder_text="Leave blank to keep current", 
            show='•', 
            width=250, 
            height=30
        )
        self.confirm_pass_entry.pack(pady=(0, 10), fill="x")
        
        # Specialty dropdown
        ctk.CTkLabel(left_frame, text="Specialty", anchor="w").pack(anchor="w", pady=(5, 2))
        self.specialty_var = ctk.StringVar(value="")
        self.specialty_dropdown = ctk.CTkComboBox(
            left_frame, 
            values=self.specialties,
            width=250,
            height=30,
            variable=self.specialty_var
        )
        self.specialty_dropdown.pack(pady=(0, 10), fill="x")
        
        # Department dropdown
        ctk.CTkLabel(left_frame, text="Department", anchor="w").pack(anchor="w", pady=(5, 2))
        self.department_var = ctk.StringVar(value="")
        self.department_dropdown = ctk.CTkComboBox(
            left_frame, 
            values=self.departments,
            width=250,
            height=30,
            variable=self.department_var
        )
        self.department_dropdown.pack(pady=(0, 10), fill="x")
        
        # Salary field
        ctk.CTkLabel(left_frame, text="Salary (€)", anchor="w").pack(anchor="w", pady=(5, 2))
        self.salary_entry = ctk.CTkEntry(
            left_frame, 
            placeholder_text="Enter annual salary", 
            width=250, 
            height=30
        )
        self.salary_entry.pack(pady=(0, 10), fill="x")
        
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
            placeholder_text="Enter name", 
            width=250, 
            height=30
        )
        self.name_entry.pack(pady=(0, 10), fill="x")
        
        # Surname field
        ctk.CTkLabel(right_frame, text="Surname", anchor="w").pack(anchor="w", pady=(5, 2))
        self.surname_entry = ctk.CTkEntry(
            right_frame, 
            placeholder_text="Enter surname", 
            width=250, 
            height=30
        )
        self.surname_entry.pack(pady=(0, 10), fill="x")
        
        # Social Security Number field (read-only)
        ctk.CTkLabel(right_frame, text="Social Security Number", anchor="w").pack(anchor="w", pady=(5, 2))
        self.ssn_entry = ctk.CTkEntry(
            right_frame,
            placeholder_text="Format: XXX-XX-XXXX",
            width=250,
            height=30,
            state="disabled"  # Make it read-only
        )
        self.ssn_entry.pack(pady=(0, 10), fill="x")
        
        # Helper text for SSN format
        ssn_helper = ctk.CTkLabel(
            right_frame,
            text="SSN cannot be modified",
            font=ctk.CTkFont(size=11),
            text_color="gray60"
        )
        ssn_helper.pack(anchor="w", pady=(0, 10))
        
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
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.grid(row=2, column=0, pady=(20, 30))
        
        # Save Changes button
        save_btn = ctk.CTkButton(
            buttons_frame, 
            text="Save Changes", 
            command=self.save_changes,
            width=150,
            height=35,
            fg_color="#003366",
            hover_color="#004080"
        )
        save_btn.pack(side="left", padx=5)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            buttons_frame, 
            text="Cancel", 
            command=lambda: controller.show_frame("AdminDoctors"),
            width=150,
            height=35,
            fg_color="#555555",
            hover_color="#666666"
        )
        cancel_btn.pack(side="left", padx=5)
    
    def validate_ssn(self, ssn):
        """Validate SSN format (XXX-XX-XXXX)"""
        pattern = r'^\d{3}-\d{2}-\d{4}$'
        return bool(re.match(pattern, ssn))
        
    def validate_salary(self, salary_str):
        """Validate and convert salary to float"""
        try:
            salary = float(salary_str)
            if salary <= 0:
                return False, "Salary must be a positive number"
            return True, salary
        except ValueError:
            return False, "Salary must be a valid number"
    
    def load_doctor_data(self):
        if hasattr(self.controller, 'selected_doctor') and self.controller.selected_doctor:
            doctor = self.controller.selected_doctor
            
            # Load personal information
            self.user_entry.configure(state="normal")
            self.user_entry.delete(0, tk.END)
            self.user_entry.insert(0, doctor.get_protected_attribute("personal_id"))
            self.user_entry.configure(state="disabled")
            
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, doctor.get_protected_attribute("name"))
            
            self.surname_entry.delete(0, tk.END)
            self.surname_entry.insert(0, doctor.get_protected_attribute("surname"))
            
            self.ssn_entry.configure(state="normal")
            self.ssn_entry.delete(0, tk.END)
            self.ssn_entry.insert(0, doctor.get("socialsecurity"))
            self.ssn_entry.configure(state="disabled")
            
            self.gender_var.set(doctor.get_protected_attribute("gender"))
            
            # Set birthday
            birthday = doctor.get_protected_attribute("birthday")
            self.birthday_entry.set_date(birthday)
            
            # Set specialty and department
            self.specialty_var.set(doctor.get("speciality"))
            self.department_var.set(doctor.get("department"))
            
            # Set salary
            self.salary_entry.delete(0, tk.END)
            self.salary_entry.insert(0, str(doctor.get("salary")))
            
            self.pass_entry.delete(0, tk.END)
            self.confirm_pass_entry.delete(0, tk.END)
            
    def save_changes(self):
        """Save the changes to the doctor in the database"""
        if not hasattr(self.controller, 'selected_doctor') or not self.controller.selected_doctor:
            messagebox.showerror("Error", "No doctor selected for modification")
            return
        
        doctor = self.controller.selected_doctor
        
        try:
            # Check password fields if provided
            password = self.pass_entry.get()
            confirm_password = self.confirm_pass_entry.get()
            
            if password or confirm_password:
                if password != confirm_password:
                    messagebox.showerror("Error", "Passwords do not match")
                    return
                
                # Update password if provided
                if password:
                    doctor.set_protected_info("password", password, 'str')
            
            # Validate name and surname
            name = self.name_entry.get()
            surname = self.surname_entry.get()
            
            if not (name and surname):
                messagebox.showerror("Error", "Name and surname cannot be empty")
                return
                
            if not (name.isalpha() and surname.isalpha()):
                messagebox.showerror("Error", "Name and surname must contain only letters")
                return
            
            # Update personal information
            doctor.set_protected_info("name", name, 'str')
            doctor.set_protected_info("surname", surname, 'str')
            doctor.set_protected_info("gender", self.gender_var.get(), 'str')
            
            # Validate birthday
            birthday = self.birthday_entry.get_date()
            if not (date(1900, 1, 1) <= birthday <= date.today()):
                raise ValueError("Birth date must be between 1900-01-01 and today")
            
            doctor.set_protected_info("birthday", birthday, 'date')
            
            # Update doctor-specific fields
            specialty = self.specialty_var.get()
            department = self.department_var.get()
            
            if not (specialty and department):
                messagebox.showerror("Error", "Specialty and department cannot be empty")
                return
                
            doctor.set("speciality", specialty, 'str')
            doctor.set("department", department, 'str')
            
            # Validate and set salary
            salary_str = self.salary_entry.get()
            
            try:
                salary = float(salary_str)
                if salary <= 0:
                    raise ValueError("Salary must be a positive number")
                
                doctor.set("salary", salary, 'float')
            except ValueError as e:
                if "could not convert string to float" in str(e):
                    raise ValueError("Salary must be a valid number")
                else:
                    raise
            
            messagebox.showinfo("Success", "Doctor information updated successfully!")
            self.controller.show_frame("AdminDoctors")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        
    def tkraise(self, *args, **kwargs):
        """Load doctor data when the frame is raised"""
        super().tkraise(*args, **kwargs)
        self.load_doctor_data()
        
