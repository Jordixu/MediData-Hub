from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
import datetime as dt
from tkcalendar import DateEntry

class PatientInformation(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Patient Information"
        
        # Configure the main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Title
        self.grid_rowconfigure(1, weight=1)  # Form content
        self.grid_rowconfigure(2, weight=0)  # Buttons
        
        # Title
        title_label = ctk.CTkLabel(
            self, 
            text="Patient Information", 
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
        
        # Personal ID field
        ctk.CTkLabel(left_frame, text="Personal ID", anchor="w").pack(anchor="w", pady=(5, 2))
        self.personal_id_entry = ctk.CTkEntry(
            left_frame, 
            width=250, 
            height=30,
            state="readonly"
        )
        self.personal_id_entry.pack(pady=(0, 10), fill="x")
        
        # Hospital ID field
        ctk.CTkLabel(left_frame, text="Hospital ID", anchor="w").pack(anchor="w", pady=(5, 2))
        self.hospital_id_entry = ctk.CTkEntry(
            left_frame, 
            width=250, 
            height=30,
            state="readonly"
        )
        self.hospital_id_entry.pack(pady=(0, 10), fill="x")
        
        # Change Password button
        change_pass_btn = ctk.CTkButton(
            left_frame, 
            text="Change Password",
            width=200,
            height=35,
            fg_color="#003366",
            hover_color="#004080",
            command=lambda: controller.show_frame("ChangePassword")
        )
        change_pass_btn.pack(pady=(15, 5))
        
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
            width=250, 
            height=30
        )
        self.name_entry.pack(pady=(0, 10), fill="x")
        
        # Surname field
        ctk.CTkLabel(right_frame, text="Surname", anchor="w").pack(anchor="w", pady=(5, 2))
        self.surname_entry = ctk.CTkEntry(
            right_frame, 
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
            date_pattern='dd/MM/yyyy'
        )
        self.birthday_entry.pack(fill="x", ipady=3)
        
        # Weight field
        ctk.CTkLabel(right_frame, text="Weight (kg)", anchor="w").pack(anchor="w", pady=(5, 2))
        self.weight_entry = ctk.CTkEntry(
            right_frame, 
            width=250, 
            height=30
        )
        self.weight_entry.pack(pady=(0, 10), fill="x")
        
        # Height field
        ctk.CTkLabel(right_frame, text="Height (cm)", anchor="w").pack(anchor="w", pady=(5, 2))
        self.height_entry = ctk.CTkEntry(
            right_frame, 
            width=250, 
            height=30
        )
        self.height_entry.pack(pady=(0, 10), fill="x")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.grid(row=2, column=0, pady=(20, 30))
        
        # Modify button
        modify_btn = ctk.CTkButton(
            buttons_frame, 
            text="Save Changes", 
            command=self.modify_data,
            width=150,
            height=35,
            fg_color="#003366",
            hover_color="#004080"
        )
        modify_btn.pack(side="left", padx=5)
        
        # Go Back button
        back_btn = ctk.CTkButton(
            buttons_frame, 
            text="Go Back", 
            command=lambda: controller.show_frame("PatientMainScreen"),
            width=150,
            height=35,
            fg_color="#555555",
            hover_color="#666666"
        )
        back_btn.pack(side="left", padx=5)
        
        # Delete User button (separate from other buttons for visual distinction)
        delete_btn = ctk.CTkButton(
            self, 
            text="Delete Account", 
            command=self.delete_patient,
            width=150,
            height=35,
            fg_color="#8B0000",
            hover_color="#B22222"
        )
        delete_btn.grid(row=3, column=0, pady=(0, 20))

    def load_data(self):
        self.name_entry.delete(0, tk.END)
        self.surname_entry.delete(0, tk.END)
        self.gender_var.set("")
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        
        try:
            self.personal_id_entry.configure(state="normal")
            self.personal_id_entry.delete(0, tk.END)
            self.personal_id_entry.insert(0, self.controller.current_user_data.get_protected_attribute("personal_id"))
            self.personal_id_entry.configure(state="readonly")
            
            self.hospital_id_entry.configure(state="normal")
            self.hospital_id_entry.delete(0, tk.END)
            self.hospital_id_entry.insert(0, self.controller.current_user_data.get_protected_attribute("hospital_id"))
            self.hospital_id_entry.configure(state="readonly")
            
            self.name_entry.insert(0, self.controller.current_user_data.get_protected_attribute("name"))
            self.surname_entry.insert(0, self.controller.current_user_data.get_protected_attribute("surname"))
            self.gender_var.set(self.controller.current_user_data.get_protected_attribute("gender"))
            birthday_str = self.controller.current_user_data.get_protected_attribute("birthday")
            birthday_date = dt.datetime.strptime(birthday_str, "%Y-%m-%d").date() if isinstance(birthday_str, str) else birthday_str
            self.birthday_entry.set_date(birthday_date)
            self.weight_entry.insert(0, self.controller.current_user_data.get("weight"))
            self.height_entry.insert(0, self.controller.current_user_data.get("height"))

        except AttributeError as exc:
            messagebox.showerror("Error", str(exc))

    def modify_data(self):
        if self.controller.current_user_data is None:
            messagebox.showerror("Error", "Data not found. You are using a test account.")
            return
        try:
            patient = self.controller.current_user_data
            patient.set_protected_info("name", self.name_entry.get(), 'str')
            patient.set_protected_info("surname", self.surname_entry.get(), 'str')
            patient.set_protected_info("gender", self.gender_var.get(), 'str')
            if not (dt.date(1900, 1, 1) <= self.birthday_entry.get_date() <= dt.date.today()):
                raise ValueError("I don't think you were born in the future or in the 19th century...")
            patient.set_protected_info("birthday", self.birthday_entry.get_date(), 'date')
            patient.set("weight", self.controller.utility.validate_and_cast_value(
                self.weight_entry.get(), float, 0, 1000,
                custom_message_incorrect_type="The weight must be a number...",
                custom_message_lower="The weight must be a positive number.",
                custom_message_upper="Did you know that the heaviest person ever recorded was 635 kg?"), 'float')
            patient.set("height", self.controller.utility.validate_and_cast_value(
                self.height_entry.get(), float, 0, 300,
                custom_message_incorrect_type="The height must be a number...",
                custom_message_lower="The height must be a positive number.",
                custom_message_upper="Are you human or giraffe?"), 'float')

            messagebox.showinfo("Success", "Information updated successfully!")
            self.controller.show_frame("PatientMainScreen")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        
    def delete_patient(self):
        message = "Are you sure you want to delete your account? This action cannot be undone."
        if messagebox.askyesno("Warning", message):
            try:
                self.controller.hospital.remove_patient(self.controller.current_user)
                messagebox.showinfo("Success", "Account deleted successfully")
                self.controller.show_frame("RoleSelectionScreen")
            except TypeError:
                messagebox.showerror("Error", "There is no data to delete since you are using a test account.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_data()