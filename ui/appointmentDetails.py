import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime as dt

class AppointmentDetails(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Appointment Details"
        
        # Configure the main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # Title
        self.grid_rowconfigure(2, weight=1)  # Content
        self.grid_rowconfigure(3, weight=0)  # Separator
        self.grid_rowconfigure(4, weight=0)  # Buttons
        
        # Title with larger font
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=1, column=0, pady=(30, 20), sticky="ew")
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="Appointment Details", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=5)
        
        # Main content area with wider spacing
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=2, column=0, padx=70, pady=20, sticky="n")
        
        # Create two columns - left and right with more space
        content_frame.grid_columnconfigure(0, weight=1, minsize=350)
        content_frame.grid_columnconfigure(1, weight=1, minsize=350)
        
        # Left column - contains basic appointment info
        left_column = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_column.grid(row=0, column=0, sticky="nw", padx=30, pady=10)
        
        # Right column - contains person info
        right_column = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_column.grid(row=0, column=1, sticky="nw", padx=30, pady=10)
        
        # Style for labels and values with larger fonts
        label_font = ctk.CTkFont(size=15, weight="bold")
        value_font = ctk.CTkFont(size=15)
        
        # Appointment ID
        appointment_id_label = ctk.CTkLabel(
            left_column, 
            text="Appointment ID:", 
            font=label_font, 
            anchor="w", 
            width=150
        )
        appointment_id_label.grid(row=0, column=0, sticky="w", padx=5, pady=15)
        
        self.appointment_id_value = ctk.CTkLabel(
            left_column, 
            text="", 
            font=value_font, 
            anchor="w"
        )
        self.appointment_id_value.grid(row=0, column=1, sticky="w", padx=5, pady=15)
        
        # Status with color indicator
        status_label = ctk.CTkLabel(
            left_column, 
            text="Status:", 
            font=label_font, 
            anchor="w", 
            width=150
        )
        status_label.grid(row=1, column=0, sticky="w", padx=5, pady=15)
        
        self.status_frame = ctk.CTkFrame(left_column, fg_color="transparent")
        self.status_frame.grid(row=1, column=1, sticky="w", padx=5, pady=15)
        
        self.status_indicator = ctk.CTkLabel(
            self.status_frame, 
            text="",
            width=16,
            height=16,
            corner_radius=8,
            fg_color="#3498db"
        )
        self.status_indicator.pack(side="left", padx=(0, 10))
        
        self.status_value = ctk.CTkLabel(
            self.status_frame, 
            text="", 
            font=value_font, 
            anchor="w"
        )
        self.status_value.pack(side="left")
        
        # Date
        date_label = ctk.CTkLabel(
            left_column, 
            text="Date:", 
            font=label_font, 
            anchor="w", 
            width=150
        )
        date_label.grid(row=2, column=0, sticky="w", padx=5, pady=15)
        
        self.date_value = ctk.CTkLabel(
            left_column, 
            text="", 
            font=value_font, 
            anchor="w"
        )
        self.date_value.grid(row=2, column=1, sticky="w", padx=5, pady=15)
        
        # Time
        time_label = ctk.CTkLabel(
            left_column, 
            text="Time:", 
            font=label_font, 
            anchor="w", 
            width=150
        )
        time_label.grid(row=3, column=0, sticky="w", padx=5, pady=15)
        
        self.time_value = ctk.CTkLabel(
            left_column, 
            text="", 
            font=value_font, 
            anchor="w"
        )
        self.time_value.grid(row=3, column=1, sticky="w", padx=5, pady=15)
        
        # Room
        room_label = ctk.CTkLabel(
            left_column, 
            text="Room:", 
            font=label_font, 
            anchor="w", 
            width=150
        )
        room_label.grid(row=4, column=0, sticky="w", padx=5, pady=15)
        
        self.room_value = ctk.CTkLabel(
            left_column, 
            text="", 
            font=value_font, 
            anchor="w"
        )
        self.room_value.grid(row=4, column=1, sticky="w", padx=5, pady=15)
        
        
        # Doctor
        doctor_label = ctk.CTkLabel(
            right_column, 
            text="Doctor:", 
            font=label_font, 
            anchor="w", 
            width=150
        )
        doctor_label.grid(row=0, column=0, sticky="w", padx=5, pady=15)
        
        self.doctor_value = ctk.CTkLabel(
            right_column, 
            text="", 
            font=value_font, 
            anchor="w"
        )
        self.doctor_value.grid(row=0, column=1, sticky="w", padx=5, pady=15)
        
        # Patient
        patient_label = ctk.CTkLabel(
            right_column, 
            text="Patient:", 
            font=label_font, 
            anchor="w", 
            width=150
        )
        patient_label.grid(row=1, column=0, sticky="w", padx=5, pady=15)
        
        self.patient_value = ctk.CTkLabel(
            right_column, 
            text="", 
            font=value_font, 
            anchor="w"
        )
        self.patient_value.grid(row=1, column=1, sticky="w", padx=5, pady=15)
        
        # Diagnosis ID
        diagnosis_id_label = ctk.CTkLabel(
            right_column, 
            text="Diagnosis ID:", 
            font=label_font, 
            anchor="w", 
            width=150
        )
        diagnosis_id_label.grid(row=2, column=0, sticky="w", padx=5, pady=15)
        
        self.diagnosis_id_value = ctk.CTkLabel(
            right_column, 
            text="", 
            font=value_font, 
            anchor="w"
        )
        self.diagnosis_id_value.grid(row=2, column=1, sticky="w", padx=5, pady=15)
        
        # Medication ID
        medication_id_label = ctk.CTkLabel(
            right_column, 
            text="Medication ID:", 
            font=label_font, 
            anchor="w", 
            width=150
        )
        medication_id_label.grid(row=3, column=0, sticky="w", padx=5, pady=15)
        
        self.medication_id_value = ctk.CTkLabel(
            right_column, 
            text="", 
            font=value_font, 
            anchor="w"
        )
        self.medication_id_value.grid(row=3, column=1, sticky="w", padx=5, pady=15)
        
        # Add a separator before the button
        separator = ttk.Separator(self, orient="horizontal")
        separator.grid(row=3, column=0, sticky="ew", pady=(30, 20), padx=30)
        
        # Button section at bottom
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=4, column=0, pady=(0, 30))
        
        # Back button - larger
        self.back_button = ctk.CTkButton(
            button_frame,
            text="Go Back",
            command=self.go_back,
            width=180,
            height=45,
            fg_color="#002D62",
            hover_color="#00458E",
            corner_radius=4,
            font=ctk.CTkFont(size=15)
        )
        self.back_button.pack(padx=10)
        
        # Status color mapping
        self.status_colors = {
            'Scheduled': '#3498db',  # Blue
            'In Progress': '#f39c12',  # Orange
            'Completed': '#2ecc71',  # Green
            'Cancelled': '#e74c3c',  # Red
            'Rescheduled': '#9b59b6',  # Purple
            'Pending': '#f1c40f',  # Yellow
            'Rejected': '#95a5a6'   # Gray
        }
        
    def process_time_tuples(self, time):
        """Convert a tuple of time strings or time objects to a single string."""
        if isinstance(time, tuple) and len(time) >= 2:
            start_time = time[0]
            end_time = time[1]
            
            # Handle different types of time representations
            if isinstance(start_time, dt.time) and isinstance(end_time, dt.time):
                return f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
            elif isinstance(start_time, str) and isinstance(end_time, str):
                return f"{start_time} - {end_time}"
            else:
                return f"{start_time} - {end_time}"
        return "N/A"
        
    def load_data(self):
        """Load the appointment data into the UI"""
        if not hasattr(self.controller, 'current_appointment') or not self.controller.current_appointment:
            messagebox.showerror("Error", "No appointment selected")
            self.go_back()
            return
            
        appointment = self.controller.current_appointment
        
        # Set basic appointment info
        appointment_id = appointment.get("appointment_id")
        self.appointment_id_value.configure(text=str(appointment_id) if appointment_id is not None else "N/A")
        
        # Status with color indicator
        status = appointment.get("status")
        status_text = status if status is not None else "N/A"
        self.status_value.configure(text=status_text)
        
        # Set status color
        status_color = self.status_colors.get(status_text, "#95a5a6")  # Default to gray if status not found
        self.status_indicator.configure(fg_color=status_color)
        
        # Format date
        date_val = appointment.get("date")
        if date_val and date_val != "N/A":
            if isinstance(date_val, dt.date):
                formatted_date = date_val.strftime("%Y-%m-%d")
            else:
                formatted_date = str(date_val)
        else:
            formatted_date = "N/A"
        self.date_value.configure(text=formatted_date)
        
        # Format time
        timeframe = appointment.get("timeframe")
        if timeframe and timeframe != "N/A":
            formatted_time = self.process_time_tuples(timeframe)
        else:
            formatted_time = "N/A"
        self.time_value.configure(text=formatted_time)
        
        # Room
        room_number = appointment.get("room_number")
        self.room_value.configure(text=str(room_number) if room_number is not None else "N/A")
        
        # Doctor
        doctor_id = appointment.get("doctor_hid")
        doctor_text = f"ID: {doctor_id}" if doctor_id is not None else "N/A"
        
        if doctor_id is not None and hasattr(self.controller.hospital, "doctors"):
            doctor = self.controller.hospital.doctors.get(doctor_id)
            if doctor:
                doctor_name = f"{doctor.get_protected_attribute('name')} {doctor.get_protected_attribute('surname')}"
                doctor_text = f"Dr. {doctor_name} (ID: {doctor_id})"
        
        self.doctor_value.configure(text=doctor_text)
        
        # Patient
        patient_id = appointment.get("patient_hid")
        patient_text = f"ID: {patient_id}" if patient_id is not None else "N/A"
        
        if patient_id is not None and hasattr(self.controller.hospital, "patients"):
            patient = self.controller.hospital.patients.get(patient_id)
            if patient:
                patient_name = f"{patient.get_protected_attribute('name')} {patient.get_protected_attribute('surname')}"
                patient_text = f"{patient_name} (ID: {patient_id})"
        
        self.patient_value.configure(text=patient_text)
        
        # Diagnosis ID
        diagnosis_id = appointment.get("diagnosis_id")
        diagnosis_text = str(diagnosis_id) if diagnosis_id is not None else "None"
        self.diagnosis_id_value.configure(text=diagnosis_text)
        
        # Medication ID
        medication_id = appointment.get("medication_id")
        medication_text = str(medication_id) if medication_id is not None else "None"
        self.medication_id_value.configure(text=medication_text)
    
    def go_back(self):
        """Return to the previous screen"""
        self.controller.current_appointment = None
        
        user_role = self.controller.selected_role
        if user_role == "doctor":
            self.controller.show_frame("DoctorAppointments")
        elif user_role == "patient":
            self.controller.show_frame("PatientAppointments")
        elif user_role == "admin":
            self.controller.show_frame("AdminAppointments")
        else:
            self.controller.show_frame("RoleSelectionScreen")
        
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_data()