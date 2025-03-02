import customtkinter as ctk
from tkinter import messagebox

class PatientRequestAppointment(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Request Appointment"
        
        # Configure the main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Title
        self.grid_rowconfigure(1, weight=0)  # Filters
        self.grid_rowconfigure(2, weight=1)  # Content
        self.grid_rowconfigure(3, weight=0)  # Buttons
        
        # Title section
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew", pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="Request New Appointment", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Filters section
        filters_frame = ctk.CTkFrame(self)
        filters_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 20))
        
        filters_frame.columnconfigure(0, weight=1)
        filters_frame.columnconfigure(1, weight=1)
        filters_frame.columnconfigure(2, weight=1)
        
        # Department selection
        dept_frame = ctk.CTkFrame(filters_frame, fg_color="transparent")
        dept_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        
        self.department_label = ctk.CTkLabel(
            dept_frame, 
            text="Department", 
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        self.department_label.pack(anchor="w", pady=(0, 5))
        
        self.department_menu = ctk.CTkComboBox(
            dept_frame, 
            values=[
                "Select Department", "ER", "Surgery", "Internal Medicine", 
                "Pediatrics", "Psychiatry", "Oncology", "Cardiology", 
                "Neurology", "Gynecology", "Urology"
            ],
            state='readonly', 
            command=self.filter_doctors,
            height=35,
            dropdown_font=ctk.CTkFont(size=13)
        )
        self.department_menu.pack(fill="x")
        self.department_menu.set("Select Department")

        # Specialty selection
        spec_frame = ctk.CTkFrame(filters_frame, fg_color="transparent")
        spec_frame.grid(row=0, column=1, padx=15, pady=15, sticky="ew")
        
        self.specialty_label = ctk.CTkLabel(
            spec_frame, 
            text="Specialty", 
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        self.specialty_label.pack(anchor="w", pady=(0, 5))
        
        self.specialty_menu = ctk.CTkComboBox(
            spec_frame, 
            values=[
                "Select Specialty", "Cardiology", "Dermatology", "Endocrinology", 
                "Gastroenterology", "Hematology", "Infectious Disease", 
                "Nephrology", "Neurology", "Oncology", "Pulmonology", 
                "Rheumatology", "Urology"
            ],
            state='readonly', 
            command=self.filter_doctors,
            height=35,
            dropdown_font=ctk.CTkFont(size=13)
        )
        self.specialty_menu.pack(fill="x")
        self.specialty_menu.set("Select Specialty")
        
        # Doctor selection
        doc_frame = ctk.CTkFrame(filters_frame, fg_color="transparent")
        doc_frame.grid(row=0, column=2, padx=15, pady=15, sticky="ew")
        
        self.selected_doctor_label = ctk.CTkLabel(
            doc_frame, 
            text="Doctor", 
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        self.selected_doctor_label.pack(anchor="w", pady=(0, 5))
        
        self.doctor_menu = ctk.CTkComboBox(
            doc_frame, 
            state='readonly', 
            values=["Select Doctor"],
            height=35,
            dropdown_font=ctk.CTkFont(size=13)
        )
        self.doctor_menu.pack(fill="x")
        self.doctor_menu.set("Select Doctor")
        
        # Content section - appointment details
        content_frame = ctk.CTkFrame(self)
        content_frame.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 20))
        
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=0)  # Title section
        content_frame.rowconfigure(1, weight=0)  # Title input
        content_frame.rowconfigure(2, weight=0)  # Description section
        content_frame.rowconfigure(3, weight=1)  # Description input
        
        # Title section
        title_section = ctk.CTkFrame(content_frame, fg_color="transparent")
        title_section.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 5))
        
        self.title_label = ctk.CTkLabel(
            title_section, 
            text="Appointment Title", 
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        self.title_label.pack(anchor="w")
        
        # Title input
        self.title_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Describe briefly the reason for the appointment",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.title_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Description section
        desc_section = ctk.CTkFrame(content_frame, fg_color="transparent")
        desc_section.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 5))
        
        self.description_label = ctk.CTkLabel(
            desc_section, 
            text="Description", 
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        self.description_label.pack(anchor="w")
        
        # Description input
        self.description_entry = ctk.CTkTextbox(
            content_frame, 
            height=200,
            wrap="word",
            font=ctk.CTkFont(size=14),
            border_width=1,
            corner_radius=6
        )
        self.description_entry.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Buttons section
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.grid(row=3, column=0, sticky="ew", padx=30, pady=(0, 30))
        
        # Cancel button
        self.cancel_button = ctk.CTkButton(
            buttons_frame, 
            text="Cancel", 
            command=lambda: controller.show_frame("PatientAppointments"),
            width=150,
            height=40,
            fg_color="#555555",
            hover_color="#666666",
            font=ctk.CTkFont(size=14)
        )
        self.cancel_button.pack(side="left", padx=(0, 10))
        
        # Send button
        self.send_button = ctk.CTkButton(
            buttons_frame, 
            text="Send Request", 
            command=self.send_request,
            width=150,
            height=40,
            fg_color="#2D5A88",
            hover_color="#1D4A78",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.send_button.pack(side="right")
        
    def filter_doctors(self, *args):
        """Filter doctors based on department and specialty selections"""
        department = self.department_menu.get()
        specialty = self.specialty_menu.get()
        
        # Reset doctor menu
        self.doctor_menu.set("Select Doctor")
        
        # Only update if meaningful selections are made
        if (department == "Select Department" or specialty == "Select Specialty"):
            self.doctor_menu.configure(values=["Select Doctor"])
            return
            
        doctors = []
        for doctor in self.controller.hospital.doctors.values():
            doctor_department = doctor.get("department")
            doctor_specialty = doctor.get("speciality")
            
            if (doctor_department == department and 
                doctor_specialty == specialty):
                doctors.append(
                    f"{doctor.get_protected_attribute('name')} "
                    f"{doctor.get_protected_attribute('surname')}"
                )
                
        if doctors:
            self.doctor_menu.configure(values=doctors)
        else:
            self.doctor_menu.configure(values=["No doctors available"])
    
    def send_request(self):
        """Handle appointment request submission"""
        selected_doctor_name = self.doctor_menu.get()
        title = self.title_entry.get().strip()
        description = self.description_entry.get("1.0", "end-1c").strip()
        
        # Validate inputs
        if selected_doctor_name == "Select Doctor" or selected_doctor_name == "No doctors available":
            messagebox.showerror("Error", "Please select a doctor")
            return
            
        if not title:
            messagebox.showerror("Error", "Please enter an appointment title")
            return
            
        if not description:
            messagebox.showerror("Error", "Please provide a description for your appointment request")
            return
            
        # Proper access through hospital object
        for doctor in self.controller.hospital.doctors.values():
            full_name = (f"{doctor.get_protected_attribute('name')} "
                        f"{doctor.get_protected_attribute('surname')}")
            
            if full_name == selected_doctor_name:
                # Create notification using proper hospital ID
                appointment_id = self.controller.hospital.request_appointment(
                                    self.controller.current_user,
                                    doctor.get_protected_attribute("hospital_id"),
                                )
                self.controller.hospital.send_notification(
                    doctor.get_protected_attribute("hospital_id"),
                    self.controller.current_user,
                    title,
                    "Appointment Request",
                    description,
                    appointment_id=appointment_id
                )
                messagebox.showinfo("Success", "Appointment request sent successfully")
                self.controller.show_frame("PatientAppointments")
                return
        
        messagebox.showerror("Error", "Selected doctor not found")
        
    def tkraise(self, *args, **kwargs):
        """Reset form when screen is shown"""
        super().tkraise(*args, **kwargs)
        
        # Reset form fields
        self.department_menu.set("Select Department")
        self.specialty_menu.set("Select Specialty")
        self.doctor_menu.set("Select Doctor")
        self.doctor_menu.configure(values=["Select Doctor"])
        self.title_entry.delete(0, "end")
        self.description_entry.delete("1.0", "end")