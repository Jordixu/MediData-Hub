import customtkinter as ctk
from tkinter import messagebox
class PatientRequestAppointment(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Personal Data"
        
        self.container_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.container_frame.pack(expand=True, fill="both")
        
        self.menu_frame = ctk.CTkFrame(self.container_frame, fg_color="transparent")
        self.menu_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.menu_frame.grid_columnconfigure(0, weight=4)
        self.menu_frame.grid_columnconfigure(1, weight=4)
        self.menu_frame.grid_columnconfigure(2, weight=4)
        self.menu_frame.grid_columnconfigure(3, weight=1)
        
        # Dropdown menus
        self.department_label = ctk.CTkLabel(self.menu_frame, text="Select Department")
        self.department_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.department_menu = ctk.CTkComboBox(self.menu_frame, values=[
            "Select Department", "ER", "Surgery", "Internal Medicine", "Pediatrics", "Psychiatry", "Oncology", "Cardiology", "Neurology", "Gynecology", "Urology"
            ], state='readonly')
        self.department_menu.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.specialty_label = ctk.CTkLabel(self.menu_frame, text="Select Specialty")
        self.specialty_label.grid(row=0, column=1, padx=10, pady=20, sticky="ew")
        self.specialty_menu = ctk.CTkComboBox(self.menu_frame, values=[
            "Select Specialty", "Cardiology", "Dermatology", "Endocrinology", "Gastroenterology", "Hematology", "Infectious Disease", "Nephrology", "Neurology", "Oncology", "Pulmonology", "Rheumatology", "Urology"
            ], state='readonly')
        self.specialty_menu.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        self.selected_doctor_label = ctk.CTkLabel(self.menu_frame, text="Select Doctor")
        self.selected_doctor_label.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        self.doctor_menu = ctk.CTkComboBox(self.menu_frame, state='readonly', values=["Select Doctor"])
        self.doctor_menu.grid(row=1, column=2, padx=10, pady=10, sticky="ew")
        
        self.update_button = ctk.CTkButton(self.menu_frame, text="Search Doctor", command=lambda: self.selected_doctors())
        self.update_button.grid(row=1, column=3, padx=10, pady=10, sticky="ew")
        
        # Text frame (title and description)
        self.text_frame = ctk.CTkFrame(self.container_frame, fg_color="transparent")
        self.text_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Title and description
        self.title_label = ctk.CTkLabel(self.text_frame, text="Title", font=("Helvetica", 14, "bold"), wraplength=500)
        self.title_label.pack(pady=10)
        self.title_entry = ctk.CTkEntry(self.text_frame, width=50, placeholder_text="Describe briefly the reason for the appointment")
        self.title_entry.pack(pady=10, expand=True, fill="both")

        self.description_label = ctk.CTkLabel(self.text_frame, text="Description", font=("Helvetica", 14, "bold"))
        self.description_label.pack(pady=10)
        self.description_entry = ctk.CTkTextbox(self.text_frame, height=250, width=50, wrap="word", border_width=2)
        self.description_entry.pack(pady=20, expand=True, fill="both")

        # Cancel and Send buttons
        self.buttons_frame = ctk.CTkFrame(self.container_frame, fg_color="transparent")
        self.buttons_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(1, weight=1)

        self.cancel_button = ctk.CTkButton(self.buttons_frame, text="Cancel", width=200, height=40, command= lambda: controller.show_frame("PatientAppointments"))
        self.cancel_button.grid(row=0, column=0, sticky="w")
        self.send_button = ctk.CTkButton(self.buttons_frame, text="Send", width=200, height=40, command=lambda: self.send_request())
        self.send_button.grid(row=0, column=1, sticky="e")
        
    def selected_doctors(self):
        self.doctor_menu.set("Select Doctor")
        doctors = []
        print("Updating doctors")
        for doctor in self.controller.hospital.doctors.values():
            department = doctor.get("department")
            specialty = doctor.get("speciality")
            
            if (department == self.department_menu.get() and 
                specialty == self.specialty_menu.get()):
                doctors.append(
                    f"{doctor.get_protected_attribute('name')} "
                    f"{doctor.get_protected_attribute('surname')}"
                )
        self.doctor_menu.configure(values=doctors)
        return
    
    def send_request(self):
        """Handle appointment request submission"""
        selected_doctor_name = self.doctor_menu.get()
        
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
                    self.title_entry.get(),
                    "Appointment Request",
                    self.description_entry.get("1.0", "end-1c"),
                    appointment_id=appointment_id
                )
                messagebox.showinfo("Success", "Request sent successfully")
                self.controller.show_frame("PatientAppointments")
                return
        
        messagebox.showerror("Error", "Selected doctor not found")